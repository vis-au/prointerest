import numpy as np
import pandas as pd
from .doi_component import DoiComponent
from sklearn.metrics.pairwise import euclidean_distances
from sklearn_extra.cluster import KMedoids


class AveragenessComponent(DoiComponent):
    def __init__(self, subspace=[]) -> None:
        super().__init__()
        self.subspace = subspace
        self.kmedoids = KMedoids(
            n_clusters=self.n_bins,
            metric="euclidean",
            method="alternate",
            init="heuristic",
            max_iter=100,
            random_state=0,
        )

    def compute_doi(self, X: pd.DataFrame):
        if len(X) == 0:
            return np.empty((0,))
            # compute the median for each dimension in self.subsapce, then compute the euclidean
            # distance

        X_ = (
            X.select_dtypes(["number"]) if len(self.subspace) == 0 else X[self.subspace]
        )
        # X_median_item = np.array(X_.median()).reshape(1, -1)

        model = self.kmedoids.fit_predict(X_)
        X_median_item = model.cluster_centers_[0]

        distances = euclidean_distances(X_, X_median_item)
        min_distance = distances.min()
        max_distance = distances.max()

        if min_distance == max_distance:
            return np.zeros((len(X),))

        # normalize distances
        doi = (distances - min_distance) / (max_distance - min_distance)
        doi = doi.reshape(
            -1,
        )

        return doi
