from typing import Any, Literal
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans

from database import *
from outlierness_component import OutliernessComponent
from provenance_component import *
from scagnostics_component import ScagnosticsComponent


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
  global SCAGNOSTIC_WEIGHTS
  SCAGNOSTIC_WEIGHTS = weights

def set_provenance_weights(weights: dict[str, float]):
  global PROVENANCE_WEIGHTS
  PROVENANCE_WEIGHTS = weights

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

outlierness_comp = OutliernessComponent()
provenance_comp = ProvenanceComponent()
scagnostics_comp = ScagnosticsComponent()


def log_interaction(mode: Literal["brush", "zoom", "select", "inspect"], items: list[any]):
  global current_interactions
  # interaction: [timestamp: number, mode: string, ids: list[number]]
  provenance_comp.add_interaction([
    current_interactions, mode, np.array(items)[:,0]
  ])
  df = pd.DataFrame(items)
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)
  df["id"] = df.index

  provenance_comp.train(df)

  current_interactions += 1


def compute_dois(items: list[list[Any]]):
  global current_chunk
  df = pd.DataFrame(items)
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)

  provenance_doi = provenance_comp.predict_doi(df)

  if current_chunk % 3 == 0:
    df["id"] = df.index
    outlierness_doi = outlierness_comp.train(df)
    # scagnostics_doi = scagnostics_comp.train(df.loc[0:10])
  else:
    outlierness_doi = outlierness_comp.predict_doi(df)
    # scagnostics_doi = scagnostics_comp.predict_doi(df)

  prior = outlierness_doi
  posterior = provenance_doi
  doi = COMPONENT_WEIGHTS["prior"] * prior + COMPONENT_WEIGHTS["posterior"] * posterior

  current_chunk += 1
  return doi


def compute_doi_classes(doi: list[list[float]]):
  X = np.array(doi).reshape(-1, 1)
  kmeans = MiniBatchKMeans(n_clusters=DOI_CLASSES, random_state=0).fit(X)
  centers = kmeans.cluster_centers_.reshape((1, -1))
  labels = kmeans.labels_
  return centers, labels