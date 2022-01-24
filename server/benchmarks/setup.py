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

from doi_components import *
from storage_strategies import *
from context_strategies import *
from update_strategies import *
from database import initialize_db, drop_tables


# load benchmark configuration
config = json.load(open("./config.json"))
doi_label = "sort"
data_label = "sorted1M"
PARAMETERS = config["parameters"][1]

# --- DATASET CONFIGURATION
DATASET = config["datasets"][data_label]
data_path = DATASET["data_path"]
column_data_path = DATASET["column_data_path"]
total_db_size = DATASET["total_db_size"]  # full size of database
n_dims = DATASET["n_dims"]  # number of dimensions in the data
numeric_columns = DATASET["numeric_columns"]  # columns used in the doi functions
id_column = "tripID"  # TODO: fixed for now

# --- DOI CONFIGURATION
doi = get_doi_component(doi_label, numeric_columns)

# --- REMAINING PARAMETERS OF THE BENCHMARKS
total_size = PARAMETERS["total_size"]  # total number of processed items, not nec. the dataset size
chunk_size = PARAMETERS["chunk_size"]  # number of new items retrieved per step
n_bins = PARAMETERS["n_bins"]  # number of bins used in doi histograms
update_size = PARAMETERS["update_size"]
context_size = PARAMETERS["context_size"]
n_chunks_context = max(context_size // chunk_size, 1)  # number of chunks considered for context
n_chunks_update = max(update_size // chunk_size, 1)  # number of chunks considered for updating
max_age = PARAMETERS["max_age"]  # maximal age of the considered chunks

chunks = round(total_size / chunk_size)  # number of steps
storage_size = chunk_size * max_age  # maximum size of storages

# load strategies
storage_strategies = get_storage_strategies(storage_size)
context_strategies = get_context_strategies(n_dims, n_chunks_context, n_bins)
update_strategies = get_update_strategies(n_dims, n_chunks_update, max_age)

short_test_case_title = f"doi: {doi_label}, items: {total_size}, chunk size: {chunk_size}"
full_test_case_title = f"{short_test_case_title}, data: {data_label},\n"\
                       f"upd. size.: {update_size}, cont. size: {context_size} bins: {n_bins},\n"\
                       f"max age: {max_age}\n"


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


def get_doi_error_df(doi_df_a: pd.DataFrame, doi_df_b: pd.DataFrame, absolute=True):
  if absolute:
    diff = pd.DataFrame(doi_df_a["doi"] - doi_df_b["doi"]).abs()
  else:
    diff = pd.DataFrame(doi_df_a["doi"] - doi_df_b["doi"])
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
