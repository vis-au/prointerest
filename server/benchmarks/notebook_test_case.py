import altair as alt

from benchmarks import load_test_case, DATASET_SUBDIR, DOI_SUBDIR, PARAMETER_SUBDIR, STRATEGY_SUBDIR
from context_strategies import get_context_strategies
from update_strategies import get_update_strategies
from test_case import get_path

# load benchmark configuration
modes = ["strategies", "dois", "datasets", "parameters"]
MODE = "strategies"  # which variable the benchmarks are run over / results are shown by
TEST_CASE_INDEX = 0

tc = load_test_case(TEST_CASE_INDEX)
DATA = tc.data
PARAMETERS = tc.params
DOI_CONFIG = tc.doi

subdir = ""
if MODE == "strategies":
  subdir = STRATEGY_SUBDIR
elif MODE == "dois":
  subdir = DOI_SUBDIR
elif MODE == "datasets":
  subdir = DATASET_SUBDIR
elif MODE == "parameters":
  subdir = PARAMETER_SUBDIR

PATH = get_path(DATA.name, DOI_CONFIG.name, PARAMETERS.total_size, PARAMETERS.chunk_size, subdir)

CONTEXT_STRATEGIES = get_context_strategies(DATA.n_dims, PARAMETERS.chunks, PARAMETERS.n_bins)
UPDATE_STRATEGIES = get_update_strategies(DATA.n_dims, PARAMETERS.chunks, PARAMETERS.max_age)

# altair visualizations use the data server extension to reduce notebook size
alt.data_transformers.enable("data_server")
