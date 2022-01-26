import os
from sys import path
import json
import altair as alt

# make this script "top level"
cwd = os.getcwd()
path.append(f"{cwd}/..")

from test_case import (DatasetConfiguration, DoiConfiguration, ParametersConfiguration,
                       get_dataset_config, get_doi_config, get_parameters_config, get_path,
                       generate_strategies)
from doi_components import *
from storage_strategies import *
from context_strategies import *
from update_strategies import *


def load_test_case(index: int):
  TEST_CASES = json.load(open("./test_cases.json"))
  test_case = TEST_CASES["test_cases"][index]


# load benchmark configuration
doi_label = "averageness"
data_label = "blobs"
parameter_label = "12k"

DATA: DatasetConfiguration = get_dataset_config(data_label)
DOI_CONFIG: DoiConfiguration = get_doi_config(doi_label, DATA)
PARAMETERS: ParametersConfiguration = get_parameters_config(parameter_label)

# create the path for storing the benchmark results if they do not exist
PATH = get_path(data_label, doi_label, PARAMETERS.total_size, PARAMETERS.chunk_size)

context_strategies, update_strategies, storage_strategies = generate_strategies(DATA, PARAMETERS)

# altair visualizations use the data server extension to reduce notebook size
alt.data_transformers.enable("data_server")
