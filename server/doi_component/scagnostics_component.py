import pandas as pd
import numpy as np
from pyscagnostics import scagnostics

from database import ID
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
        self.scores = pd.DataFrame(columns=[ID] + list(self.weights.keys()))

    def get_doi(self, ids: np.ndarray):
        if len(ids) == 0:
            return np.empty((0, ))

        # this is a sanity check, in case this function is called "on-demand", finding only those
        # ids that we actually have scores for
        available_scores = self.scores.loc[self.scores[ID].isin(ids)]

        doi = np.zeros((len(available_scores), ))

        for measure in self.weights:
            doi += self.weights[measure] * available_scores[measure]

        return doi

    def compute_doi(self, X: pd.DataFrame):
        if len(X) == 0:
            return np.empty((0, ))

        X_ = X.select_dtypes(["number"]) if len(self.subspace) == 0 else X[self.subspace]

        # get scagnostics scores for the input along the current axes in the plot
        scores, _ = scagnostics(X[self.subspace[0]].to_numpy(), X[self.subspace[1]].to_numpy())

        # score names produced by the library have upper case first letter key, so we need to fit
        # those to the labels used in self.weights
        scores = {key.lower(): value for key, value in scores.items()}

        scores_df = pd.DataFrame(columns=self.scores.columns)
        scores_df[ID] = X[0]  # first column in df is id column

        for measure in self.weights:
            scores_df[measure] = scores[measure]

        # save the scores for fast retrieval for when the user adjusts the weights
        self.scores = pd.concat([self.scores, scores_df], ignore_index=True)

        # the doi value then is just multiplying the weights with the scores
        doi = self.get_doi(scores_df[ID])

        return doi
