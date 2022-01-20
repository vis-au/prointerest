import os
from os.path import exists
from sys import path
import numpy as np
import pandas as pd
import altair as alt

# make this script "top level"
cwd = os.getcwd()
path.append(f"{cwd}/..")

from doi_component.sort_component import SortComponent
from doi_component.outlierness_component import OutliernessComponent
from doi_component.density_component import DensityComponent

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


# --- BENCHMARK CONFIGURATION
# doi = OutliernessComponent(["0", "1"])
# doi_label = "outlierness"
# doi = SortComponent(["0", "1"])
# doi_label = "sort"
doi = DensityComponent(bandwidth=5)
doi_label = "density"

total_size = 10200  # total number of processed items, not nec. the size of the data
chunk_size = 100  # number of new items retrieved per step
chunks = round(total_size / chunk_size)  # number of steps
no_bins = 10  # number of bins used in doi histograms

n_chunks = 3  # number of chunks considered for context/updating
max_age = 20  # maximal age of the considered chunks
storage_size = chunk_size * max_age  # maximum size of storages

# --- USE CASE CONFIGURATION
# data_label = "taxis"
# data_path = "../data/nyc_taxis.shuffled_full.csv.gz"
# column_data_path = "../data/nyc_taxis.shuffled_full.parquet"
# data_label = "blobs"
# data_path = "../data/blobs.csv"
# column_data_path = "../data/nyc_taxis.shuffled_full.parquet"  # not used, but required
data_label = "swiss_roll"
data_path = "../data/swiss_roll.csv"
column_data_path = "../data/nyc_taxis.shuffled_full.parquet"  # not used, but required

id_column = "tripID"
# total_db_size = 112145904  # full size of database
total_db_size = 1000000  # full size of database
# n_dims = 17  # number of dimensions in the data
n_dims = 2


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
    n_dims=n_dims, n_clusters=chunk_size, n_samples_per_cluster=n_chunks, storage=None
  ))
]

# altair visualizations use the data server extension to reduce notebook size
alt.data_transformers.enable("data_server")

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


# helper function that bins the doi column
def get_doi_bins_df(doi_df: pd.DataFrame, with_labels=False) -> pd.DataFrame:
  histogram, edges = np.histogram(doi_df["doi"], bins=no_bins, range=(0, 1))
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
  delta_bins["bin"] = delta_bins.index / no_bins
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
    # process_chunk_callback=taxi_process_chunk
  )


# compute the ratio and duration in s per ride in the taxi dataset
def taxi_process_chunk(chunk: pd.DataFrame):
  dropoff = chunk["tpep_dropoff_datetime"]
  pickup = chunk["tpep_pickup_datetime"]
  chunk["duration"] = dropoff - pickup
  chunk["duration"] = chunk["duration"].apply(lambda x: x.total_seconds())
  chunk["ratio"] = chunk["tip_amount"] / chunk["total_amount"]
  return chunk
