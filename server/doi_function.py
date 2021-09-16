from typing import Any, Literal
import pandas as pd
import numpy as np

from database import *
from outlierness_component import OutliernessComponent


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


def set_dimensions_of_interest(dimensions: list[str]):
  global dimensions_of_interest
  dimensions_of_interest = dimensions

def set_dimension_range_of_interest(dimension: str, min_value: float, max_value: float):
  global ranges_of_interest
  ranges_of_interest[dimension] = [min_value, max_value]

def set_outlierness_metric(metric: str):
  global outlierness_metric
  outlierness_metric = metric

def set_selected_item_ids(ids: list[any]):
  mark_ids_selected(ids)


def set_scagnostic_weights(weights: dict[str, float]):
  global SCAGNOSTIC_WEIGHTS
  SCAGNOSTIC_WEIGHTS = weights


def set_provenance_items(ids: list[str], doi: list[float]):
  # mark_ids_provenance(ids, doi)
  pass


# INTEREST COMPUTATION

i = 0
outlierness = OutliernessComponent()
def compute_dois(items: list[list[Any]]):
  global i
  df = pd.DataFrame(items)
  df = df.drop(columns=[2, 3, 7, 18, 19])
  df = df.astype(np.float64)

  if i % 3 == 0:
    df["id"] = df.index
    doi = outlierness.train(df)
  else:
    doi = outlierness.predict_doi(df)

  i += 1
  return doi