from typing import Callable
import pandas as pd
import numpy as np

from .doi_component import DoiComponent


class FeatureComponent(DoiComponent):
    weights: dict  # prioritization between the doi dimensions, dim->float with sum=1
    intervals: dict  # interesting ranges [min, max] dim -> float
    get_dimensions_in_data: Callable  # overloaded getter function for dimensions in the dataset

    def __init__(
        self,
        weights: dict = {},
        intervals: dict = {},
        get_dimensions_in_data: Callable = lambda _: [],
    ):
        super().__init__()
        self.weights = weights
        self.intervals = intervals
        self.get_dimensions_in_data = get_dimensions_in_data

    def compute_doi(self, X: pd.DataFrame):
        """
        Computes the degree of interest per item over the dimensions of interest and accompanying
        weights. Items that match all intervals get the highest interest, and items that only match
        some dimensions get a lower score.
        """
        # HACK: convert the dimension labels into numbers, because the input data only has indeces
        dimensions = self.get_dimensions_in_data()
        subspace = list(self.weights.keys())
        X_ = X[subspace]
        X_mask = np.zeros_like(X_)

        for i, dimension in enumerate(self.weights):
            # assume everything to be interesting if no interval is provided
            interval = (
                self.intervals[dimension]
                if dimension in self.intervals
                else [float("-inf"), float("inf")]
            )

            min_value = interval[0]
            max_value = interval[1]

            # create boolean index whether a row matches the filter for that dimension
            X_mask[:, i] = (X[dimension] >= min_value) & (X[dimension] <= max_value)

            # instead of [0, 1], use the provided weight if the dimension matches
            X_mask[:, i] = X_mask[:, i] * self.weights[dimension]

        X_mask = X_mask.sum(axis=1).reshape(
            (-1, 1)
        )  # sum over weights where rows match filters
        return X_mask
