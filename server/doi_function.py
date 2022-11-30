from typing import Literal, List, Tuple
import pandas as pd
import numpy as np

from database import *
from doi_component.scagnostics_component import *
from doi_component.feature_component import *
from context_item_selection_strategy.context_item_selection_strategy import *
from outdated_item_selection_strategy.outdated_item_selection_strategy import *
from doi_component.provenance_component import ProvenanceComponent
from context_item_selection_strategy.doi_based_context import DoiBasedContext
from storage_strategy.windowing_storage import WindowingStorage
from storage_strategy.storage_strategy import StorageStrategy


# INTEREST COMPUTATION
STORAGE_SIZE = 100000
current_chunk = 0
current_interactions = 0

# contains the weights for the dimensions used in the DOI function
DIMENSION_WEIGHTS = {}

# contains the interesting value ranges within each dimension
DIMENSION_INTERVALS = {}

scagnostics_comp = ScagnosticsComponent([5, 17])  # FIXME: unused, but kept for compatibility
provenance_comp = ProvenanceComponent()  # FIXME: unused, but kept for legacy compatibility

feature_comp: DoiComponent = FeatureComponent(
  weights=DIMENSION_WEIGHTS,
  intervals=DIMENSION_INTERVALS,
  get_dimensions_in_data=get_dimensions_in_data
)
doi_component: DoiComponent = feature_comp

storage: StorageStrategy = WindowingStorage(STORAGE_SIZE)
context: ContextItemSelectionStrategy = DoiBasedContext(n_dims=20, storage=storage, n_bins=25)
update: OutdatedItemSelectionStrategy = None


def reset_doi_component():
  global storage, context
  storage = WindowingStorage(STORAGE_SIZE)
  context = DoiBasedContext(n_dims=20, storage=storage, n_bins=25)


def set_component_weights(weights: dict):
  # FIXME: legacy function
  # COMPONENT_WEIGHTS["prior"] = weights["prior"]
  # COMPONENT_WEIGHTS["posterior"] = weights["posterior"]
  return


def set_prior_weights(weights: dict):
  # FIXME: legacy function
  # global PRIOR_WEIGHTS
  # PRIOR_WEIGHTS = weights
  return


def set_posterior_weights(weights: dict):
  # FIXME: legacy function
  # global POSTERIOR_WEIGHTS
  # POSTERIOR_WEIGHTS = weights
  return


def set_scatterplot_axis(axis: str, dimension: int):
  # subspace = scagnostics_comp.subspace

  # if axis == "x":
  #   subspace[0] = dimension
  # elif axis == "y":
  #   subspace[1] = dimension

  # scagnostics_comp.subspace = subspace
  return


def set_scagnostic_weights(weights: dict):
  scagnostics_comp.weights = weights


def set_provenance_weights(weights: dict):
  provenance_comp.weights = weights


def set_outlierness_weights(weights: dict):
  # FIXME: legacy function
  # outlierness_comp.weights = weights
  return


def set_dimension_weights(weights: dict):
  global DIMENSION_WEIGHTS

  DIMENSION_WEIGHTS = {}

  for dimension in weights:
    DIMENSION_WEIGHTS[dimension] = weights[dimension]

  feature_comp.weights = DIMENSION_WEIGHTS


def set_dimension_range_of_interest(dimension: str, min_value: float, max_value: float):
  global DIMENSION_INTERVALS

  if min_value is None or max_value is None:
    # if the frontend sets the interesting range to INFINITY, this corresponds to None here
    # for simplicity, we treat INFINITY the same as having no interest at all.
    del DIMENSION_INTERVALS[dimension]
    return

  DIMENSION_INTERVALS[dimension] = [min_value, max_value]
  feature_comp.intervals = DIMENSION_INTERVALS


def set_doi_classes(classes: int):
  global DOI_CLASSES
  DOI_CLASSES = classes


def set_dimensions_of_interest(dimensions: list):
  global dimensions_of_interest
  dimensions_of_interest = dimensions


def set_outlierness_metric(metric: str):
  global outlierness_metric
  outlierness_metric = metric


def set_scagnostic_weights(weights: dict):
  scagnostics_comp.weights = weights


def log_interaction(mode: Literal["brush", "zoom", "select", "inspect"], items: list):
  global current_interactions
  provenance_comp.add_interaction([
    current_interactions, mode, np.array(items)[:, 0]
  ])
  df = pd.DataFrame(items)
  df = df.drop(columns=[2, 3, 7, 18, 19])  # non-numerical columns
  df = df.astype(np.float64)
  df["id"] = df.index

  current_interactions += 1


CONTEXT_SIZE: int = 1000
UPDATE_INTERVAL: int = 10


def doi_f(chunk_with_context: np.ndarray):
  df = pd.DataFrame(chunk_with_context)
  df = df.drop(columns=[2, 3, 7, 18, 19])  # non-numerical columns
  df = df.astype(np.float64)

  df["id"] = df.index

  doi = doi_component.compute_doi(df)

  return doi


def compute_dois(items: list) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
  global current_chunk

  X = np.array(items)

  context_items = context.get_context_items(CONTEXT_SIZE, current_chunk)
  updated_ids = context_items[ID].tolist() if len(context_items) > 0 else []

  X_ = np.concatenate((X, context_items), axis=0)
  dois_with_context = doi_f(X_)
  new_dois = dois_with_context[:len(X)]
  updated_dois = dois_with_context[len(X):]

  df = pd.DataFrame(items)
  df.rename(columns={0: ID}, inplace=True)
  storage.insert_chunk(df, current_chunk)

  current_chunk += 1
  return new_dois, updated_ids, updated_dois
