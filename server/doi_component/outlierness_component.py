import pandas as pd
import numpy as np

from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from .doi_component import DoiComponent


# adapted from https://scikit-learn.org/stable/modules/outlier_detection.html
class OutliernessComponent(DoiComponent):
    def __init__(self, subspace: list[int]=None, outlierness_fraction: int=0.15) -> None:
        super().__init__()
        self.subspace = subspace
        self.outliers_fraction = outlierness_fraction
        self.outlierness_measures = self._generate_measures()
        self.current_interest: pd.DataFrame = None
        # the columns of the dataframe to be considered for outlierness
        self.weights = {"elliptic": 0.25, "oneclass": 0.25, "forest": 0.25, "lof": 0.25}

    def _generate_measures(self):
        return [
            EllipticEnvelope(contamination=self.outliers_fraction),
            OneClassSVM(nu=self.outliers_fraction, gamma=0.1),
            IsolationForest(contamination=self.outliers_fraction, random_state=0),
            LocalOutlierFactor(n_neighbors=10, contamination=self.outliers_fraction)
        ]

    def compute_doi(self, X: pd.DataFrame):
        if len(X) == 0:
            return np.empty((0, ))

        if self.subspace is not None:
            X_ = X[self.subspace].to_numpy()
        else:
            X_ = X.to_numpy()

        predictions = np.array(
            [
                (self.outlierness_measures[0].fit(X_).predict(X_)).astype(int),
                (self.outlierness_measures[1].fit(X_).predict(X_)).astype(int),
                (self.outlierness_measures[2].fit(X_).predict(X_)).astype(int),
                (self.outlierness_measures[3].fit_predict(X_)).astype(int),
            ]
        )

        # -1 is outlier, 1 is inlier, so for doi, we need to adjust this to [0, 1]
        predictions[predictions == 1] = 0
        predictions[predictions == -1] = 1

        weights = np.array(
            [
                self.weights["elliptic"],
                self.weights["oneclass"],
                self.weights["forest"],
                self.weights["lof"]
            ]
        ).reshape(len(predictions), 1)

        doi = (predictions * weights).sum(axis=0)

        return doi
