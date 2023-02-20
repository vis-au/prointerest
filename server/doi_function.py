from typing import List, Literal

import numpy as np
import pandas as pd

from database import ID, ID_INDEX, get_dimensions_in_data
from doi_component.doi_component import DoiComponent
from doi_component.feature_component import FeatureComponent
from doi_component.interaction_component import InteractionComponent
from doi_component.numeric_dimension_component import NumericDimensionComponent
from doi_component.provenance_component import ProvenanceComponent
from doi_component.scagnostics_component import ScagnosticsComponent

# INTEREST COMPUTATION
STORAGE_SIZE = 100000

current_chunk_no = 0  # keeps track of how "old" the latest data is
current_interactions_count = 0  # keeps track of how many interactions took place

# contains the weights for the dimensions used in the DOI function
DIMENSION_WEIGHTS = {}

# contains the interesting value ranges within each dimension
DIMENSION_INTERVALS = {}

scagnostics_comp = ScagnosticsComponent(
    [5, 17]
)  # FIXME: unused, but kept for compatibility
provenance_comp = (
    ProvenanceComponent()
)  # FIXME: unused, but kept for legacy compatibility


def create_feature_component():
    return FeatureComponent(
        weights=DIMENSION_WEIGHTS,
        intervals=DIMENSION_INTERVALS,
        get_dimensions_in_data=get_dimensions_in_data,
    )


def create_dimension_component():
    return NumericDimensionComponent(
        weights=DIMENSION_WEIGHTS,
        get_dimensions_in_data=get_dimensions_in_data,
    )


feature_comp: DoiComponent = create_feature_component()
dimension_comp: DoiComponent = create_dimension_component()
interaction_comp = InteractionComponent()


def reset_doi_component():
    global feature_comp, dimension_comp, DIMENSION_INTERVALS, DIMENSION_WEIGHTS

    DIMENSION_INTERVALS = {}
    DIMENSION_WEIGHTS = {}
    feature_comp = create_feature_component()
    dimension_comp = create_dimension_component()
    interaction_comp.clear()


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
    dimension_comp.weights = DIMENSION_WEIGHTS


def set_dimension_intervals(intervals: dict):
    global DIMENSION_INTERVALS
    DIMENSION_INTERVALS = {}

    for dimension in intervals:
        DIMENSION_INTERVALS[dimension] = intervals[dimension]

    feature_comp.intervals = DIMENSION_INTERVALS


def set_dimension_interval(dimension: str, min_value: float, max_value: float):
    global DIMENSION_INTERVALS

    if min_value is None or max_value is None:
        # if the frontend sets the interesting range to INFINITY, this corresponds to None here
        # for simplicity, we treat INFINITY the same as having no interest at all.
        if dimension in DIMENSION_INTERVALS:
            del DIMENSION_INTERVALS[dimension]
        return

    DIMENSION_INTERVALS[dimension] = [min_value, max_value]
    feature_comp.intervals = DIMENSION_INTERVALS


def set_doi_classes(classes: int):
    global DOI_CLASSES
    DOI_CLASSES = classes


def set_dimensions_of_interest(dimensions: List[str]):
    global dimensions_of_interest
    dimensions_of_interest = dimensions


def set_outlierness_metric(metric: str):
    global outlierness_metric
    outlierness_metric = metric


def set_scagnostic_weights(weights: dict):
    scagnostics_comp.weights = weights


def log_interaction(
    mode: Literal["scat-brush", "zoom", "select", "inspect"], items: List[str]
):
    global current_interactions_count

    provenance_comp.add_interaction(
        [current_interactions_count, mode, np.array(items)[:, 0]]
    )
    df = pd.DataFrame(items)
    df = df.drop(columns=[2, 3, 7, 18, 19])  # non-numerical columns
    df = df.astype(np.float64)
    df["id"] = df.index

    if mode in ["scat-brush", "select"]:
        interaction_comp.log_interaction(list(np.array(items)[:, ID_INDEX]))
        interaction_comp.undo_outdated_interactions()

    current_interactions_count += 1


def compute_dois(df: pd.DataFrame) -> np.ndarray:
    global current_chunk_no

    # remove non-numerical columns as they crash the tree's training step
    drop_cols = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "store_and_fwd_flag",
    ]
    df = df.drop(columns=drop_cols)
    df = df.astype(np.float32)

    # for legacy purposes, replace the dolumns with a numbered index
    dois = dimension_comp.compute_doi(df)
    if len(DIMENSION_INTERVALS) > 0:
        dois = dois * 0.5 + feature_comp.compute_doi(df) * 0.5

    return dois
