import os
from os.path import exists
from sys import path
import json
import numpy as np
import pandas as pd
import altair as alt

# make this script "top level"
cwd = os.getcwd()
path.append(f"{cwd}/..")

from doi_component.sort_component import SortComponent
from doi_component.outlierness_component import OutliernessComponent
from doi_component.density_component import DensityComponent
from doi_component.averageness_component import AveragenessComponent
from doi_component.scagnostics_component import ScagnosticsComponent

from database import initialize_db, drop_tables

from storage_strategy.no_storage import *
from storage_strategy.compression_storage import *
from storage_strategy.progressive_bin_sampler import *
from storage_strategy.reservoir_sampling_storage import *
from storage_strategy.windowing_storage import *

from outdated_item_selection_strategy.no_update import *
from outdated_item_selection_strategy.oldest_chunks_update import *
from outdated_item_selection_strategy.last_n_chunks_update import *
from outdated_item_selection_strategy.regular_interval_update import *
from outdated_item_selection_strategy.outdated_bin_update import *

from context_item_selection_strategy.no_context import *
from context_item_selection_strategy.chunk_based_context import *
from context_item_selection_strategy.sampling_based_context import *
from context_item_selection_strategy.clustering_based_context import *
from context_item_selection_strategy.doi_based_context import DoiBasedContext


# load benchmark configuration
config = json.load(open("./config.json"))
doi_label = config["doi_functions"][0]
DATASET = config["datasets"][2]
PARAMETERS = config["parameters"][1]

# --- DATASET CONFIGURATION
data_label = DATASET["data_label"]
data_path = DATASET["data_path"]
column_data_path = DATASET["column_data_path"]
total_db_size = DATASET["total_db_size"]  # full size of database
n_dims = DATASET["n_dims"]  # number of dimensions in the data
numeric_columns = DATASET["numeric_columns"]  # columns used in the doi functions
id_column = "tripID"  # TODO: fixed for now

# --- DOI CONFIGURATION
doi = DensityComponent(numeric_columns, bandwidth=5) if doi_label == "density"\
  else SortComponent(numeric_columns) if doi_label == "sort"\
  else OutliernessComponent(numeric_columns) if doi_label == "outlierness"\
  else AveragenessComponent(numeric_columns) if doi_label == "averageness"\
  else ScagnosticsComponent(numeric_columns)

# --- REMAINING PARAMETERS OF THE BENCHMARKS
total_size = PARAMETERS["total_size"]  # total number of processed items, not nec. the dataset size
chunk_size = PARAMETERS["chunk_size"]  # number of new items retrieved per step
n_bins = PARAMETERS["n_bins"]  # number of bins used in doi histograms
n_chunks = PARAMETERS["n_chunks"]  # number of chunks considered for context/updating
max_age = PARAMETERS["max_age"]  # maximal age of the considered chunks

chunks = round(total_size / chunk_size)  # number of steps
storage_size = chunk_size * max_age  # maximum size of storages

short_test_case_title = f"doi: {doi_label}, items: {total_size}, chunk size: {chunk_size}"
full_test_case_title = f"{short_test_case_title}, data: {data_label},\n"\
                       f"chunk/strat.: {n_chunks}, bins: {n_bins}, max age: {max_age}\n"


# create the path for storing the benchmark results if they do not exist
path = f"./out/{data_label}/{doi_label}/{total_size}/{chunk_size}"
if not exists("./out"):
  os.mkdir("./out")
if not exists(f"./out/{data_label}"):
  os.mkdir(f"./out/{data_label}")
if not exists(f"./out/{data_label}/{doi_label}"):
  os.mkdir(f"./out/{data_label}/{doi_label}")
if not exists(f"./out/{data_label}/{doi_label}/{total_size}"):
  os.mkdir(f"./out/{data_label}/{doi_label}/{total_size}")
if not exists(path):
  os.mkdir(path)

# all strategies are below
storage_strategies = [
  ("no_storage_strategy", NoStorage()),
  ("compression_strategy", CompressionStorage(max_size=storage_size)),
  ("progressive_bin_sampler", ProgressiveBinSampler()),
  ("reservoir_sampling_strategy", ReservoirSamplingStorage(max_size=storage_size)),
  ("windowing_strategy", WindowingStorage(max_size=storage_size))
]

update_strategies = [
  ("no update", lambda: NoUpdate(
    n_dims=n_dims, storage=None
  )),
  ("oldest n chunks", lambda: OldestChunksUpdate(
    n_dims=n_dims, storage=None, n_chunks=n_chunks, max_age=max_age
  )),
  ("last n chunks", lambda: LastNChunksUpdate(
    n_dims=n_dims, storage=None, n_chunks=n_chunks
  )),
  ("regular intervals", lambda: RegularIntervalUpdate(
    n_dims=n_dims, storage=None, n_chunks=n_chunks, max_age=max_age
  )),
  # ("outdated bins", OutdatedBinUpdate(n_dims=n_dims, storage=None))
]

context_strategies = [
  ("no context", lambda: NoContext(
    n_dims=n_dims, storage=None
  )),
  ("random chunk based", lambda: RandomChunkBasedContext(
    n_dims=n_dims, n_chunks=n_chunks, storage=None
  )),
  ("most recent chunk based", lambda: MostRecentChunkBasedContext(
    n_dims=n_dims, n_chunks=n_chunks, storage=None
  )),
  ("sampling based", lambda: RandomSamplingBasedContext(
    n_dims=n_dims, n_samples=chunk_size * n_chunks, storage=None
  )),
  ("clustering based", lambda: ClusteringBasedContext(
    n_dims=n_dims, n_clusters=n_chunks, n_samples_per_cluster=chunk_size, storage=None
  )),
  ("doi based", lambda: DoiBasedContext(
    n_dims=n_dims, n_bins=n_bins, n_samples=n_chunks*chunk_size, storage=None
  )),
]

# altair visualizations use the data server extension to reduce notebook size
alt.data_transformers.enable("data_server")


# helper function that bins the doi column
def get_doi_bins_df(doi_df: pd.DataFrame, with_labels=False) -> pd.DataFrame:
  histogram, edges = np.histogram(doi_df["doi"], bins=n_bins, range=(0, 1))
  bins_df = pd.DataFrame(histogram.transpose())

  if with_labels:
    labels = np.digitize(doi_df["doi"], bins=edges)
    return bins_df, labels
  else:
    return bins_df


# compute the difference bins
def get_doi_delta_bins_df(doi_bins_a: pd.DataFrame, doi_bins_b: pd.DataFrame):
  # copy the first df
  delta_bins = pd.DataFrame(doi_bins_a)
  delta_bins["delta"] = (doi_bins_a[0] - doi_bins_b[0]) / total_size
  delta_bins.columns = ["doi", "delta"]
  # delta_bins["delta"] = bins_a[0]

  # add context info
  delta_bins["bin"] = delta_bins.index / n_bins
  return delta_bins


# get the aboslute difference in assigned bin per item between the two dfs
def get_doi_bin_error_df(doi_bin_labels_a: pd.DataFrame, doi_bin_labels_b: pd.DataFrame):
  diff_df = pd.DataFrame(doi_bin_labels_a - doi_bin_labels_b, columns=["diff"]).abs()
  diff_df = diff_df.groupby("diff").size().reset_index()
  diff_df.columns = ["diff", "count"]
  return diff_df


def get_doi_error_df(doi_df_a: pd.DataFrame, doi_df_b: pd.DataFrame):
  diff = pd.DataFrame(doi_df_a["doi"] - doi_df_b["doi"]).abs()
  return diff


# wipe the databases that track doi, processed, update chunks, etc.
def reset():
  drop_tables()
  initialize_db(
    row_data_path=data_path,
    column_data_path=column_data_path,
    id_column=id_column,
    total_size=total_db_size,
    process_chunk_callback=taxi_process_chunk if "taxis" in data_label else None
  )


# compute the ratio and duration in s per ride in the taxi dataset
def taxi_process_chunk(chunk: pd.DataFrame):
  dropoff = chunk["tpep_dropoff_datetime"]
  pickup = chunk["tpep_pickup_datetime"]
  chunk["duration"] = dropoff - pickup
  chunk["duration"] = chunk["duration"].apply(lambda x: x.total_seconds())
  chunk["ratio"] = chunk["tip_amount"] / chunk["total_amount"]
  return chunk
