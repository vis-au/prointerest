# Prior interest components
from typing import Any
from database import *


PRIOR_WEIGHTS = {
  "dimensions": .33,
  "outlierness": .33,
  "selection": .33
}
DIMENSIONS_OF_INTEREST: list[str] = []
OUTLIERNESS_METRIC: str = "scagnostic"

def set_prior_weights(weights: dict[str, float]):
  global PRIOR_WEIGHTS
  PRIOR_WEIGHTS = weights

def set_dimensions_of_interest(dimensions: list[str]):
  global DIMENSIONS_OF_INTEREST
  DIMENSIONS_OF_INTEREST = dimensions

def set_outlierness_metric(metric: str):
  global OUTLIERNESS_METRIC
  OUTLIERNESS_METRIC = metric

def set_selected_item_ids(ids: list[any]):
  mark_ids_selected(ids)


# Posterior interest components
POSTERIOR_WEIGHTS = {
  "provenance": .5,
  "scagnostics": .5
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


def set_posterior_weights(weights: dict[str, float]):
  global POSTERIOR_WEIGHTS
  POSTERIOR_WEIGHTS = weights


def set_scagnostic_weights(weights: dict[str, float]):
  global SCAGNOSTIC_WEIGHTS
  SCAGNOSTIC_WEIGHTS = weights


def set_provenance_items(ids: list[str], doi: list[float]):
  mark_ids_provenance(ids, doi)


# INTEREST COMPUTATION
def get_dimension_interest(item: any):
  # determine if the item's values lie within the selected ranges of interest across the dimensions.
  return 0


def get_outlierness_interest(item: any):
  # using the current outlierness metric, determine if this item is an outlier. If so, return 1,
  # otherwise return 0.
  return 0


def get_selection_interest(item: any):
  # determine if the item's id is in the list of selected item ids
  item_id = item[0]
  is_selected = is_id_selected(item_id)
  return 1 if is_selected else 0


def get_scagnostic_interest(item: any):
  # compute the impact on the different weighted scagnostic measures and return it.
  return 0


def get_provenance_interest(item: any):
  # determine if the item's id is in the latest update of items that the user interacted with and if
  # so, return its interest measure. Otherwise return 0
  item_id = item[0]
  if is_id_in_provenance(item_id):
    return get_id_from_provenance(item_id)[1]
  else:
    return 0


def compute_dois(items: list[list[Any]]):
  return [[item[0], compute_doi(item)] for item in items]


def compute_doi(item: list[Any]):
  # compute prior interests
  dimension = get_dimension_interest(item)
  outlierness = get_outlierness_interest(item)
  selection = get_selection_interest(item)
  # compute posterior interests
  scagnostic = get_scagnostic_interest(item)
  provenance = get_provenance_interest(item)

  # compute combined interest
  doi = selection * PRIOR_WEIGHTS["selection"] * provenance * POSTERIOR_WEIGHTS["provenance"]
  return doi