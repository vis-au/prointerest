import pandas as pd
import numpy as np

from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

from .doi_component import DoiComponent

# adapted from https://scikit-learn.org/stable/modules/outlier_detection.html
class OutliernessComponent(DoiComponent):
    def __init__(self, subspace: list[int] = None) -> None:
        super().__init__()
        self.outliers_fraction = 0.15
        self.outlierness_measures = self._generate_measures()
        self.current_interest: pd.DataFrame = None
        # the columns of the dataframe to be considered for outlierness
        self.subspace = subspace
        self.weights = {"elliptic": 0.33, "oneclass": 0.33, "forest": 0.33}

    def _generate_measures(self):
        return [
            EllipticEnvelope(contamination=self.outliers_fraction),
            svm.OneClassSVM(nu=self.outliers_fraction, kernel="rbf", gamma=0.1),
            IsolationForest(contamination=self.outliers_fraction, random_state=0),
            # LocalOutlierFactor(n_neighbors=35, contamination=self.outliers_fraction)
        ]

    def compute_doi(self, X: pd.DataFrame):
        if self.subspace is not None:
            X_ = X[self.subspace].to_numpy()
        else:
            X_ = X.to_numpy()

        predictions = np.array(
            [
                (self.outlierness_measures[0].fit(X_).predict(X_) == -1).astype(int),
                (self.outlierness_measures[1].fit(X_).predict(X_) == -1).astype(int),
                (self.outlierness_measures[2].fit(X_).predict(X_) == -1).astype(int),
            ]
        )
        weights = np.array(
            [self.weights["elliptic"], self.weights["oneclass"], self.weights["forest"]]
        ).reshape(3, 1)

        sum = (predictions * weights).sum(axis=0)
        scaled = sum / len(predictions)

        return scaled
