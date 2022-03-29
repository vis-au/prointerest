from benchmarks import load_test_case
from context_strategies import get_context_strategies
from update_strategies import get_update_strategies
from test_case import get_path

# load benchmark configuration
# available modes: ["strategies", "dois", "datasets", "parameters"]
MODE = "strategies"  # which variable the benchmarks are run over / results are shown by
TEST_CASE_INDEX = 1

tc = load_test_case(TEST_CASE_INDEX)
DATA = tc.data
PARAMETERS = tc.params
DOI_CONFIG = tc.doi

PATH = get_path(DATA.name, DOI_CONFIG.name, PARAMETERS.total_size, PARAMETERS.chunk_size)

CONTEXT_STRATEGIES = get_context_strategies(
  DATA.n_dims,
  PARAMETERS.chunks,
  PARAMETERS.n_bins
)
UPDATE_STRATEGIES = get_update_strategies(
  DATA.n_dims,
  PARAMETERS.chunks,
  PARAMETERS.max_age,
  PARAMETERS.n_bins
)
