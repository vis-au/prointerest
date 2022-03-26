import pandas as pd
import numpy as np
from pyscagnostics import scagnostics

from .doi_component import DoiComponent


SCAGNOSTICS = [
    "Outlying",
    "Skewed",
    "Clumpy",
    "Sparse",
    "Striated",
    "Convex",
    "Skinny",
    "Stringy",
    "Monotonic",
]
SCATTERPLOT_AXES: dict = {"x": None, "y": None}


class ScagnosticsComponent(DoiComponent):
    def __init__(self, subspace: list) -> None:
        super().__init__()
        self.subspace = subspace
        self.weights = {
            "outlying": 0.11,
            "skewed": 0.11,
            "clumpy": 0.11,
            "sparse": 0.11,
            "striated": 0.11,
            "convex": 0.11,
            "skinny": 0.11,
            "stringy": 0.11,
            "monotonic": 0.11,
        }

    def compute_doi(self, X: pd.DataFrame):
        if len(X) == 0:
            return np.empty((0, ))

        X_ = X.select_dtypes(["number"]) if len(self.subspace) == 0 else X[self.subspace]

        # get scagnostics for the input
        results = scagnostics(X_)

        # calling scagnostics on a dataframe computes scagnostics for all pairwise subspaces, which
        # are all bundled up in the result object. For the doi function, we compute the mean across
        # all these subspaces:
        subspace_measures = []
        for x_dim, y_dim, result in results:
            measures, _ = result  # second element are bins
            subspace_measures += [measures]

        mean_scagnostics = pd.DataFrame(subspace_measures).mean()  # one value per component

        # measures produced by the library have upper case first letter key, so we need to fit those
        # to the labels used in self.weights
        mean_scagnostics = {key.lower(): value for key, value in mean_scagnostics.items()}

        doi = 0
        for measure in self.weights:
            doi += self.weights[measure] * mean_scagnostics[measure]

        print(self.weights)

        doi_ = np.empty((len(X), ))[:]
        doi_[:] = doi
        return doi_
