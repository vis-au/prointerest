# Prior interest components
PRIOR_WEIGHTS = {
  "dimensions": 0,
  "outlierness": 0,
  "selection": 0
}
DIMENSIONS_OF_INTEREST: list[str] = []
OUTLIERNESS_METRIC: str = "scagnostic"
SELECTED_ITEMS: list[any] = []

def set_prior_weights(weights: dict[str, float]):
  global PRIOR_WEIGHTS
  PRIOR_WEIGHTS = weights

def set_dimension_interest(dimensions: list[str]):
  global DIMENSIONS_OF_INTEREST
  DIMENSIONS_OF_INTEREST = dimensions

def set_outlierness_metric(metric: str):
  global OUTLIERNESS_METRIC
  OUTLIERNESS_METRIC = metric

def set_selected_items(items: list[any]):
  global SELECTED_ITEMS
  SELECTED_ITEMS = items


# Posterior interest components
POSTERIOR_WEIGHTS = {
  "provenance": 0,
  "scagnostics": 0
}
SCAGNOSTIC_WEIGHTS = {
  "outlying": 0,
  "skewed": 0,
  "clumpy": 0,
  "sparse": 0,
  "striated": 0,
  "convex": 0,
  "skinny": 0,
  "stringy": 0,
  "monotonic": 0
}
PROVENANCE_ITEMS = []

def set_posterior_weights(weights: dict[str, float]):
  global POSTERIOR_WEIGHTS
  POSTERIOR_WEIGHTS = weights

def set_scagnostic_weights(weights: dict[str, float]):
  global SCAGNOSTIC_WEIGHTS
  SCAGNOSTIC_WEIGHTS = weights

def set_provenance_items(items: list[any]):
  global PROVENANCE_ITEMS
  PROVENANCE_ITEMS = items


# INTEREST COMPUTATION
def get_dimension_interest(item: any):
  return 0

def get_outlierness_interest(item: any):
  return 0

def get_selection_interest(item: any):
  return 0

def get_scagnostic_interest(item: any):
  return 0

def get_provenance_interest(item: any):
  return 0

def get_interest(item: any):
  # prior
  dimension = get_dimension_interest(item) * PRIOR_WEIGHTS["dimensions"]
  outlierness = get_outlierness_interest(item) * PRIOR_WEIGHTS["outlierness"]
  selection = get_selection_interest(item) * PRIOR_WEIGHTS["selection"]
  # posterior
  scagnostic = get_scagnostic_interest(item) * POSTERIOR_WEIGHTS["provenance"]
  provenance = get_provenance_interest(item) * POSTERIOR_WEIGHTS["scagnostics"]

  # combined interest
  prior = dimension * outlierness * selection
  posterior = scagnostic * provenance

  return prior * posterior