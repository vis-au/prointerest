import os
from sys import path
import json
import altair as alt

# make this script "top level"
cwd = os.getcwd()
path.append(f"{cwd}/..")

from test_case import get_path
from doi_components import *
from storage_strategies import *
from context_strategies import *
from update_strategies import *


# load benchmark configuration
PRESETS = json.load(open("./presets.json"))
doi_label = "averageness"
data_label = "blobs"
PARAMETERS = PRESETS["parameters"][1]

# --- DATASET CONFIGURATION
DATASET = PRESETS["datasets"][data_label]
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
update_interval = PARAMETERS["update_interval"]  # number of chunks before a full update occurs

chunks = round(total_size / chunk_size)  # number of steps
storage_size = chunk_size * max_age  # maximum size of storages
# create the path for storing the benchmark results if they do not exist
path = get_path(data_label, doi_label, total_size, chunk_size)

# load strategies
storage_strategies = get_storage_strategies(storage_size)
context_strategies = get_context_strategies(n_dims, n_chunks_context, n_bins)
update_strategies = get_update_strategies(n_dims, n_chunks_update, max_age)

short_test_case_title = f"doi: {doi_label}, items: {total_size}, chunk size: {chunk_size}"
full_test_case_title = f"{short_test_case_title}, data: {data_label},\n"\
                       f"upd. size.: {update_size}, cont. size: {context_size} bins: {n_bins},\n"\
                       f"max age: {max_age}\n"

# altair visualizations use the data server extension to reduce notebook size
alt.data_transformers.enable("data_server")
