from itertools import product
from time import time
from dataclasses import dataclass
import pandas as pd
import numpy as np

from storage_strategy.storage_strategy import StorageStrategy
from storage_strategy.windowing_storage import WindowingStorage
from database import get_next_chunk_from_db, save_dois, ID, DATA_DB

from database import create_tables, drop_tables, reset_progression
from doi_function import (
    reset_doi_component,
    set_dimension_intervals,
    set_dimension_weights,
)
from doi_function import compute_dois
from server import taxi_process_chunk
from doi_regression_model import DoiRegressionModel


CHUNK_SIZE = 1000
WEIGHTS = {
    "trip_distance": 0.25,
    "total_amount": 0.25,
    "tip_amount": 0.25,
    "trip_duration": 0.25,
}
INTERVALS = {
    "trip_distance": [16, 20],
    "total_amount": [34, 74],
    "tip_amount": [4, 12],
    "trip_duration": [3, 5],
}


def get_next_progressive_result(
    storage: StorageStrategy,
    get_context=None,
    chunk_size: int = CHUNK_SIZE,
    chunk_no: int = 0,
    model: DoiRegressionModel = None
):
    """Wrapper function for getting a new chunk, computing the DOI function on it and storing the
    data for later retrieval in the storage."""

    # get chunk and compute context
    if model is not None:
        query = model.get_steering_query(table_name=DATA_DB)
        chunk_df = get_next_chunk_from_db(chunk_size, as_df=True, filters=query)

        if len(chunk_df) < chunk_size:
            unsteered_df = get_next_chunk_from_db(chunk_size - len(chunk_df), as_df=True)
            chunk_df = pd.concat([unsteered_df, chunk_df], ignore_index=True)
    else:
        chunk_df = get_next_chunk_from_db(chunk_size, as_df=True)

    context_df = pd.DataFrame([], columns=chunk_df.columns)
    if get_context is not None:
        context_df = get_context()

    # compute the DOI over chunk + context
    df = pd.concat([chunk_df, context_df], ignore_index=True)
    dois = compute_dois(df)  # HACK: compatibility with DoiComponent class
    new_dois = dois[: len(chunk_df)]

    storage.insert_chunk(chunk_df, chunk_no)
    save_dois(ids=chunk_df[ID].tolist(), dois=new_dois.reshape((-1,)).tolist())

    return chunk_df, new_dois


def reset(weights: dict, intervals: dict):
    drop_tables()

    create_tables(
        row_data_path="../data/nyc_taxis.shuffled_full.csv.gz",
        column_data_path="../data/nyc_taxis.shuffled_full.parquet",
        id_column="tripID",
        total_size=112145904,
        process_chunk_callback=taxi_process_chunk,
    )

    reset_progression()
    reset_doi_component()
    set_dimension_weights(weights)
    set_dimension_intervals(intervals)


@dataclass
class Benchmark:
    max_depths: int = 3
    n_chunks: int = 25
    chunk_size: int or range = CHUNK_SIZE
    context_size: int or range = 0
    context_strats: str or list = "stratified"
    intervals: int or range = 0
    include_previous_chunks_in_training: bool or list = True
    measure_doi_error: bool = False
    measure_timings: bool = False
    update_dois_after_training: bool = True
    storages = []

    def _compute_doi_error_stats(self, storage: StorageStrategy):
        all_items_df = storage.get_available_items()

        ground_truth_dois = pd.DataFrame(all_items_df[ID])
        ground_truth_dois["doi"] = compute_dois(all_items_df)
        ground_truth_dois.set_index(ID, inplace=True)

        stored_dois = storage.get_available_dois(with_ids=True)
        stored_dois = pd.DataFrame(stored_dois, columns=[ID, "doi"])
        stored_dois.set_index(ID, inplace=True)

        df = ground_truth_dois.join(stored_dois, lsuffix="gt", rsuffix="stored")

        # if storage is empty, then doistored is empty, causing an error in the subtraction
        if pd.isnull(df["doistored"].iloc[0]):
            return pd.Series([0], dtype="float64").describe()
        else:
            return (df["doigt"] - df["doistored"].astype(np.float64)).describe()

    def _get_test_cases(self):
        # creates full cartesian product product of the iterable test variables
        max_depths = (
            self.max_depths if type(self.max_depths) is range else [self.max_depths]
        )
        test_n_chunks = (
            self.n_chunks if type(self.n_chunks) is range else [self.n_chunks]
        )
        chunk_sizes = (
            self.chunk_size if type(self.chunk_size) is range else [self.chunk_size]
        )
        context_sizes = (
            self.context_size
            if type(self.context_size) is range
            else [self.context_size]
        )
        intervals = (
            self.intervals if type(self.intervals) is range else [self.intervals]
        )
        context_strats = (
            self.context_strats
            if type(self.context_strats) is list
            else [self.context_strats]
        )
        update_dois_after_trainings = (
            self.update_dois_after_training
            if type(self.update_dois_after_training) is list
            else [self.update_dois_after_training]
        )
        include_previous_chunks_in_training = (
            self.include_previous_chunks_in_training
            if type(self.include_previous_chunks_in_training) is list
            else [self.include_previous_chunks_in_training]
        )

        return product(
            max_depths,
            chunk_sizes,
            context_sizes,
            intervals,
            test_n_chunks,
            context_strats,
            update_dois_after_trainings,
            include_previous_chunks_in_training
        )

    def run(self):
        scores = []

        test_cases = self._get_test_cases()

        now = None  # stores timing information

        for (
            max_depth,
            chunk_size,
            context_size,
            interval,
            n_chunks,
            context_strat,
            update_dois_after_training,
            include_previous_chunks_in_training
        ) in test_cases:
            reset(intervals=INTERVALS, weights=WEIGHTS)

            storage = WindowingStorage(max_size=10000000)
            model = DoiRegressionModel(
                storage,
                max_depth=max_depth,
                include_previous_chunks_in_training=include_previous_chunks_in_training
            )

            for i in range(n_chunks):
                # measure the runtime by timing before and after the computation
                if self.measure_timings:
                    now = time()

                # no context on first iteration because storage is empty
                if i == 0:
                    chunk_df, new_dois = get_next_progressive_result(
                        storage,
                        chunk_size=chunk_size,
                        chunk_no=i,
                    )
                    model.update(chunk_df, new_dois)
                # ... otherwise use context
                else:
                    chunk_df, new_dois = get_next_progressive_result(
                        storage,
                        chunk_size=chunk_size,
                        chunk_no=i,
                        get_context=lambda: model.get_context_items(
                            context_size, context_strat
                        ),
                    )

                score = pd.Series(
                    {
                        "max_depth": max_depth,
                        "chunk_size": chunk_size,
                        "context_size": context_size,
                        "context_strat": context_strat,
                        "interval": interval,
                        "n_chunks": n_chunks,
                        "chunk": i,
                        "include_previous_chunks_in_training": include_previous_chunks_in_training,
                        "score": model.score(chunk_df, new_dois),
                    }
                )

                if self.measure_timings:
                    score["time"] = now - time()

                if self.measure_doi_error:
                    error_stats = self._compute_doi_error_stats(storage)
                    score["error_mean"] = error_stats["mean"]
                    score["error_std"] = error_stats["std"]
                    score["error_min"] = error_stats["min"]
                    score["error_max"] = error_stats["max"]

                if i == 0 or interval == 0 or i % interval == 0:
                    model.update(chunk_df, new_dois, update_dois_after_training)

                scores += [score]

            self.storages += [storage]

        return pd.DataFrame(scores)
