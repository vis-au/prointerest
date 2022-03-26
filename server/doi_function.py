from typing import Literal
import pandas as pd
import numpy as np

from database import *
from doi_component.scagnostics_component import *
from context_item_selection_strategy.context_item_selection_strategy import *
from outdated_item_selection_strategy.outdated_item_selection_strategy import *
from doi_component.provenance_component import ProvenanceComponent
from storage_strategy.storage_strategy import StorageStrategy


# INTEREST COMPUTATION
current_chunk = 0
current_interactions = 0

provenance_comp = ProvenanceComponent()
scagnostics_comp = ScagnosticsComponent([5, 17])

doi_component: DoiComponent = scagnostics_comp
context: ContextItemSelectionStrategy = None
update: OutdatedItemSelectionStrategy = None
storage: StorageStrategy = None


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


def set_scagnostic_weights(weights: dict):
  scagnostics_comp.weights = weights


def set_provenance_weights(weights: dict):
  provenance_comp.weights = weights


def set_outlierness_weights(weights: dict):
  # FIXME: legacy function
  # outlierness_comp.weights = weights
  return


def set_doi_classes(classes: int):
  global DOI_CLASSES
  DOI_CLASSES = classes


def set_dimensions_of_interest(dimensions: list):
  global dimensions_of_interest
  dimensions_of_interest = dimensions


def set_dimension_range_of_interest(dimension: str, min_value: float, max_value: float):
  global ranges_of_interest
  ranges_of_interest[dimension] = [min_value, max_value]


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
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)
  df["id"] = df.index

  current_interactions += 1


CONTEXT_SIZE: int = 1000
UPDATE_INTERVAL: int = 10


def doi_f(X: np.ndarray):
  df = pd.DataFrame(X)
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)

  df["id"] = df.index

  # TODO: use the scagnostics doi function instead
  # doi = np.random.rand(len(X), 1)
  # compute scagnostics in context
  # context_items = pd.DataFrame(context.get_context_items(CONTEXT_SIZE, current_chunk))
  # chunk_with_context = pd.concat([df, context_items])
  doi = doi_component.compute_doi(df)

  # print(doi)

  # compute scagnostics without context
  # difference is the interest for all items in the new chunk?

  return doi


def compute_dois(items: list) -> np.ndarray:
  global current_chunk
  X = np.array(items)

  dois = doi_f(X)

  current_chunk += 1
  return dois, np.zeros_like(dois), np.zeros_like(dois)  # FIXME: returns legacy doi bins and labels
