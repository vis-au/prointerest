from typing import Callable
from pandas import DataFrame
import numpy as np
from sklearn.preprocessing import normalize

from .doi_component import DoiComponent


class NumericDimensionComponent(DoiComponent):
    weights: dict
    get_dimensions_in_data: Callable

    def __init__(
        self,
        weights: dict = {},
        get_dimensions_in_data: Callable = lambda _: [],
    ) -> None:
        super().__init__()
        self.weights = weights
        self.get_dimensions_in_data = get_dimensions_in_data

    def compute_doi(self, X: DataFrame):
        """
        Computes the degree of interest per item ovoer the dimensions of interest and accompanying
        weights. Items with greater values along the selected values are assigned greater interest
        than items with lower values.
        """
        # HACK: convert the dimension labels into numbers, because the input data only has indeces
        subspace = list(self.weights.keys())
        X_ = X[subspace]

        # sets the DOI value per dimension
        X_normalized = normalize(X_, axis=0, norm="max")
        weights = np.array(list(self.weights.values()))
        X_weighted = X_normalized * weights.T
        X_sum = np.sum(X_weighted, axis=1).reshape((-1, 1))

        return X_sum
