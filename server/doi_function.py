from typing import Any, Literal
import pandas as pd
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer

from database import *
from outlierness_component import *
from provenance_component import *
from scagnostics_component import *
from progressive_bin_sampler import ProgressiveBinSampler


COMPONENT_WEIGHTS = {
  "prior": 0.5,
  "posterior": 0.5
}
PRIOR_WEIGHTS = {
  "dimensions": .33,
  "outlierness": .33,
  "selection": .33
}
POSTERIOR_WEIGHTS = {
  "provenance": .5,
  "scagnostics": .5
}

DOI_CLASSES = 10 # number of clusters the doi values are grouped into

dimensions_of_interest: list[str] = []
ranges_of_interest: dict[str, float] = {}
outlierness_metric: Literal["scagnostic", "tukey", "clustering"] = "scagnostic"


def set_component_weights(weights: dict[str, list[float]]):
  COMPONENT_WEIGHTS["prior"] = weights["prior"]
  COMPONENT_WEIGHTS["posterior"] = weights["posterior"]

def set_prior_weights(weights: dict[str, list[float]]):
  global PRIOR_WEIGHTS
  PRIOR_WEIGHTS = weights

def set_posterior_weights(weights: dict[str, float]):
  global POSTERIOR_WEIGHTS
  POSTERIOR_WEIGHTS = weights

def set_scagnostic_weights(weights: dict[str, float]):
  scagnostics_comp.weights = weights

def set_provenance_weights(weights: dict[str, float]):
  provenance_comp.weights = weights

def set_outlierness_weights(weights: dict[str, float]):
  outlierness_comp.weights = weights

def set_doi_classes(classes: int):
  global DOI_CLASSES
  DOI_CLASSES = classes


def set_dimensions_of_interest(dimensions: list[str]):
  global dimensions_of_interest
  dimensions_of_interest = dimensions

def set_dimension_range_of_interest(dimension: str, min_value: float, max_value: float):
  global ranges_of_interest
  ranges_of_interest[dimension] = [min_value, max_value]

def set_outlierness_metric(metric: str):
  global outlierness_metric
  outlierness_metric = metric


# INTEREST COMPUTATION
current_chunk = 0
current_interactions = 0

progressive_sampler = ProgressiveBinSampler(n_dims=20) # taxi dataset has 20 dimensions
outlierness_comp = OutliernessComponent([5, 17])
provenance_comp = ProvenanceComponent()
scagnostics_comp = ScagnosticsComponent()


def log_interaction(mode: Literal["brush", "zoom", "select", "inspect"], items: list[any]):
  global current_interactions
  provenance_comp.add_interaction([
    current_interactions, mode, np.array(items)[:,0]
  ])
  df = pd.DataFrame(items)
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)
  df["id"] = df.index

  current_interactions += 1

items_processed = 0
def compute_dois(items: list[list[Any]]):
  global current_chunk
  X = np.array(items)

  if items_processed == 0:
    sample = np.empty((0, X.shape[1]))
  else:
    progressive_sampler.get_current_sample()

  X_ = np.append(sample, X, axis=0)

  df = pd.DataFrame(X_)
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)

  df["id"] = df.index
  outlierness_doi = outlierness_comp.train(df)

  prior = outlierness_doi
  posterior = 0
  doi = COMPONENT_WEIGHTS["prior"] * prior + COMPONENT_WEIGHTS["posterior"] * posterior

  _, labels, edges = progressive_sampler.add_chunk(X_, doi, items_processed, compute_edges=True)

  current_chunk += 1
  return doi, labels, edges


def compute_doi_bin_edges(doi: np.ndarray, bins: np.ndarray):
  # est = KBinsDiscretizer(n_bins=DOI_CLASSES, encode="ordinal", strategy="kmeans")
  bins = progressive_sampler._bin(np.array(doi))
  edges = progressive_sampler.get_bin_edges(doi, bins)
  return edges


def compute_doi_prediction_error(items: list[list[Any]]):
  df = pd.DataFrame(items)
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)
  df["id"] = df.index

  error = outlierness_comp.get_prediction_error(df)
  print(error)
  print(error.mean())
  return error