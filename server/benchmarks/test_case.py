import os
from dataclasses import dataclass

from progressive_doi_pipeline import ProgressiveDoiPipeline
from database import initialize_db, drop_tables

from doi_component.doi_component import DoiComponent
from context_item_selection_strategy.context_item_selection_strategy import *
from context_item_selection_strategy.no_context import *
from outdated_item_selection_strategy.outdated_item_selection_strategy import *
from outdated_item_selection_strategy.no_update import *
from storage_strategy.storage_strategy import *
from storage_strategy.no_storage import NoStorage
from storage_strategy.windowing_storage import WindowingStorage


@dataclass
class TestCase:
  name: str
  doi: DoiComponent
  context_strategy: ContextItemSelectionStrategy
  update_strategy: OutdatedItemSelectionStrategy
  storage_strategy: StorageStrategy
  doi_label: str
  data_label: str
  data_path: str
  column_data_path: str
  id_column: str
  chunk_size: int
  context_size: int
  update_size: int
  chunks: int
  total_size: int
  update_interval: int
  doi_csv_path: str
  times_csv_path: str
  pipeline: ProgressiveDoiPipeline = None

  def run(self) -> None:
    reset(
      self.data_path,
      self.data_label,
      self.column_data_path,
      self.id_column,
      self.total_size,
    )
    self.pipeline = ProgressiveDoiPipeline(
      name=self.name,
      doi=self.doi,
      storage_strategy=self.storage_strategy,
      context_strategy=self.context_strategy,
      update_strategy=self.update_strategy,
      chunk_size=self.chunk_size,
      context_size=self.context_size,
      update_size=self.update_size,
      chunks=self.chunks
    )
    self.pipeline.run(
      doi_csv_path=self.doi_csv_path,
      times_csv_path=self.times_csv_path,
      update_interval=self.update_interval
    )
    return self.pipeline


def run_ground_truth_test_case(doi_label: str, doi: DoiComponent, data_label: str, n_dims: int,
                               total_size: int, row_path: str, column_path: str, id_column: str,
                               path: str):
  ground_truth_test_case = TestCase(
    name="__ground_truth__",
    data_label=data_label,
    id_column=id_column,
    data_path=row_path,
    column_data_path=column_path,
    doi_label=doi_label,
    doi=doi,
    storage_strategy=NoStorage(),
    context_strategy=NoContext(n_dims, None),
    update_strategy=NoUpdate(n_dims, None),
    update_interval=0,
    chunk_size=total_size,
    context_size=0,
    update_size=0,
    chunks=1,
    total_size=total_size,
    doi_csv_path=f"{path}/doi/",
    times_csv_path=None,
  )
  return ground_truth_test_case.run()


def run_bigger_chunks_test_case(doi_label: str, doi: DoiComponent, data_label: str, n_dims: int,
                                chunk_size: int, update_size: int, context_size: int,
                                total_size: int, row_path: str, column_path: str, id_column: str,
                                path: str):
  bigger_chunks_test_case = TestCase(
    name="__bigger_chunks__",
    doi=doi,
    data_label=data_label,
    id_column=id_column,
    data_path=row_path,
    column_data_path=column_path,
    doi_label=doi_label,
    storage_strategy=NoStorage(),
    context_strategy=NoContext(n_dims, None),
    update_strategy=NoUpdate(n_dims, None),
    update_interval=0,
    chunk_size=chunk_size + update_size + context_size,
    context_size=0,
    update_size=0,
    chunks=round(total_size // (chunk_size + update_size + context_size)),
    total_size=total_size,
    doi_csv_path=f"{path}/doi/",
    times_csv_path=None
  )
  return bigger_chunks_test_case.run()


def create_test_case(name: str, data_label: str, doi_label: str, data_path: str,
                     column_data_path: str, id_column: str, doi: DoiComponent, s: StorageStrategy,
                     c: ContextItemSelectionStrategy, u: OutdatedItemSelectionStrategy,
                     chunk_size: int, context_size: int, update_size: int, update_interval: int,
                     path: str, chunks: int, total_size: int) -> TestCase:

  doi_csv_path = f"{path}/doi/"
  times_csv_path = f"{path}/times/"

  return TestCase(
    name=name,
    data_label=data_label,
    data_path=data_path,
    column_data_path=column_data_path,
    id_column=id_column,
    doi_label=doi_label,
    doi=doi,
    storage_strategy=s,
    context_strategy=c,
    update_strategy=u,
    chunk_size=chunk_size,
    context_size=context_size,
    update_size=update_size,
    chunks=chunks,
    total_size=total_size,
    update_interval=update_interval,
    doi_csv_path=doi_csv_path,
    times_csv_path=times_csv_path,
  )


def get_path(data_label: str, doi_label: str, total_size: int, chunk_size: int) -> str:
  path = f"./out/{data_label}/{doi_label}/{total_size}/{chunk_size}"

  if not os.path.exists("./out"):
    os.mkdir("./out")
  if not os.path.exists(f"./out/{data_label}"):
    os.mkdir(f"./out/{data_label}")
  if not os.path.exists(f"./out/{data_label}/{doi_label}"):
    os.mkdir(f"./out/{data_label}/{doi_label}")
  if not os.path.exists(f"./out/{data_label}/{doi_label}/{total_size}"):
    os.mkdir(f"./out/{data_label}/{doi_label}/{total_size}")
  if not os.path.exists(path):
    os.mkdir(path)

  return path


def run_test_case_from_config(config: dict, context_strategies: list[ContextItemSelectionStrategy],
                              update_strategies: list[OutdatedItemSelectionStrategy],
                              skip_if_exists: bool = True) -> None:

  for doi_label in config.doi_functions:
    for parameters in config.parameters:
      parameter_label = parameters["parameter_label"]
      update_interval = parameters["update_interval"]
      chunk_size = parameters["chunk"]
      total_size = parameters["total_size"]
      chunks = round(total_size / chunk_size)

      for d_ in config.datasets:
        dataset = config.datasets[d_]
        data_label = dataset["data_label"]
        path = get_path(data_label, doi_label, total_size, chunk_size)

        for context_ in context_strategies:
          context_label = context_[0]
          context_strategy = context_[1]

          for update_ in update_strategies:
            update_label = update_[0]
            update_strategy = update_[1]

            label = f"{context_label}-{update_label}"
            if skip_if_exists and path.isfile(f"{path}/doi/{label}.csv"):
              print("skipping test case because already completed.")
              continue

            test_case = create_test_case(
              # name=f"{doi_label}{data_label}{context_label}{update_label}",
              name=label,
              doi_label=doi_label,
              storage_strategy=WindowingStorage(max_size=total_size),
              context_strategy=context_strategy,
              update_strategy=update_strategy,
              chunk_size=chunk_size,
              chunks=chunks,
              update_interval=update_interval,
              path=path
            )

            test_case.run()


# compute the ratio and duration in s per ride in the taxi dataset
def taxi_process_chunk(chunk: pd.DataFrame):
  dropoff = chunk["tpep_dropoff_datetime"]
  pickup = chunk["tpep_pickup_datetime"]
  chunk["duration"] = dropoff - pickup
  chunk["duration"] = chunk["duration"].apply(lambda x: x.total_seconds())
  chunk["ratio"] = chunk["tip_amount"] / chunk["total_amount"]
  return chunk


# wipe the databases that track doi, processed, update chunks, etc.
def reset(data_path: str, data_label: str, column_data_path: str, id_column: str,
          total_size: int) -> None:
  drop_tables()
  initialize_db(
    row_data_path=data_path,
    column_data_path=column_data_path,
    id_column=id_column,
    total_size=total_size,
    process_chunk_callback=taxi_process_chunk if "taxis" in data_label else None
  )
