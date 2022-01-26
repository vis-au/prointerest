import os
from sys import path
import altair as alt

# make this script "top level" to allow importing database module, etc.
if True:
  cwd = os.getcwd()
  path.append(f"{cwd}/..")

from test_case import (DatasetConfiguration, DoiConfiguration, ParametersConfiguration,
                       get_dataset_config, get_doi_config, get_parameters_config, get_path,
                       generate_strategies)


# load benchmark configuration
doi_label = "averageness"
data_label = "blobs"
parameter_label = "120"

DATA: DatasetConfiguration = get_dataset_config(data_label)
DOI_CONFIG: DoiConfiguration = get_doi_config(doi_label, DATA)
PARAMETERS: ParametersConfiguration = get_parameters_config(parameter_label)

# create the path for storing the benchmark results if they do not exist
PATH = get_path(data_label, doi_label, PARAMETERS.total_size, PARAMETERS.chunk_size)

context_strategies, update_strategies, storage_strategies = generate_strategies(DATA, PARAMETERS)

# altair visualizations use the data server extension to reduce notebook size
alt.data_transformers.enable("data_server")
