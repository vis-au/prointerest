from typing import List, Literal, Tuple

import numpy as np
import pandas as pd
from context_item_selection_strategy.context_item_selection_strategy import (
    ContextItemSelectionStrategy,
)
from context_item_selection_strategy.sampling_based_context import (
    RandomSamplingBasedContext,
)
from context_item_selection_strategy.doi_based_context import DoiBasedContext
from database import ID, ID_INDEX, get_dimensions_in_data
from doi_component.doi_component import DoiComponent
from doi_component.feature_component import FeatureComponent
from doi_component.interaction_component import InteractionComponent
from doi_component.provenance_component import ProvenanceComponent
from doi_component.scagnostics_component import ScagnosticsComponent
from outdated_item_selection_strategy.outdated_item_selection_strategy import (
    OutdatedItemSelectionStrategy,
)
from sklearn.tree import DecisionTreeRegressor
from storage_strategy.storage_strategy import StorageStrategy
from storage_strategy.windowing_storage import WindowingStorage

# INTEREST COMPUTATION
CONTEXT_SIZE = 1000
UPDATE_INTERVAL = 10
STORAGE_SIZE = 100000
TREE_TRAINING_SIZE = 50000

current_chunk_no = 0  # keeps track of how "old" the latest data is
current_interactions_count = 0  # keeps track of how many interactions took place

# contains the weights for the dimensions used in the DOI function
DIMENSION_WEIGHTS = {}

# contains the interesting value ranges within each dimension
DIMENSION_INTERVALS = {}

# model for predicting the degree of interest function
regtree = DecisionTreeRegressor(random_state=0)

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


feature_comp: DoiComponent = create_feature_component()
interaction_comp = InteractionComponent()

storage: StorageStrategy = WindowingStorage(STORAGE_SIZE)
context: ContextItemSelectionStrategy = RandomSamplingBasedContext(
    n_dims=20, storage=storage
)
update: OutdatedItemSelectionStrategy = None


def reset_doi_component():
    global storage, context, feature_comp, DIMENSION_INTERVALS
    storage = WindowingStorage(STORAGE_SIZE)
    context = DoiBasedContext(n_dims=20, storage=storage, n_bins=25)

    DIMENSION_INTERVALS = {}
    feature_comp = create_feature_component()
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


def set_dimension_range_of_interest(dimension: str, min_value: float, max_value: float):
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


def doi_f(X: np.ndarray):
    df = pd.DataFrame(X)
    df = df.drop(columns=[2, 3, 7, 18, 19])  # non-numerical columns
    df = df.astype(np.float64)

    df["id"] = df.index

    # FIXME: currently uses hardcoded 50/50 weights between the two doi components
    # doi = feature_comp.compute_doi(df) * 0.5 + interaction_comp.compute_doi(df) * 0.5
    doi = feature_comp.compute_doi(df)

    return doi


def doi_prediction(X: np.ndarray):
    df = pd.DataFrame(X)
    df = df.drop(columns=[2, 3, 7, 18, 19])  # non-numerical columns
    df = df.astype(np.float64)

    doi = regtree.predict(df).reshape(
        -1,
    )

    return doi


def compute_dois(
    items: list, use_doi_f: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    global current_chunk_no

    X = np.array(items)

    context_items = context.get_context_items(CONTEXT_SIZE, current_chunk_no)
    context_ids = context_items[ID].tolist() if len(context_items) > 0 else []

    X_ = np.concatenate((X, context_items), axis=0)

    dois_with_context = doi_f(X_) if use_doi_f else doi_prediction(X_)

    new_dois = dois_with_context[: len(X)]
    updated_dois = dois_with_context[len(X) :]

    df = pd.DataFrame(items)
    df.rename(columns={0: ID}, inplace=True)
    storage.insert_chunk(df, current_chunk_no)

    current_chunk_no += 1
    return new_dois, context_ids, updated_dois


def full_doi_update(use_doi_f: bool = False) -> np.ndarray:
    """Update the DOI for every single item in storage."""

    df = storage.get_available_items()
    ids = df[ID]
    # df.columns = list(range(len(df.columns)))
    X = df.to_numpy()

    doi = doi_f(X) if use_doi_f else doi_prediction(X)

    return ids, doi


def retrain_dt() -> None:
    """Retrain the regression tree model."""
    global regtree

    df = context.get_context_items(TREE_TRAINING_SIZE, current_chunk_no)
    df.columns = list(range(len(df.columns)))
    y = doi_f(df)

    df = df.drop(columns=[2, 3, 7, 18, 19])

    regtree = DecisionTreeRegressor(random_state=0, max_depth=3)
    regtree.fit(df, y)

    return None
