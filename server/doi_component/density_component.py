import numpy as np
import pandas as pd
from doi_component.doi_component import DoiComponent
from sklearn.neighbors import KDTree


class DensityComponent(DoiComponent):
    def __init__(self, subspace: list, bandwidth=1) -> None:
        super().__init__()
        self.subspace: list = subspace
        self.bandwidth: int = bandwidth

    def compute_doi(self, X: pd.DataFrame):
        if len(X) == 0:
            return np.empty((0,))

        # get the relevant slice of the data for computing the kdtree
        X_ = (
            X.select_dtypes(["number"]) if len(self.subspace) == 0 else X[self.subspace]
        )

        kdtree = KDTree(X_)
        density = kdtree.kernel_density(X_, self.bandwidth)

        # normalize the density
        min_ = density.min()
        max_ = density.max()

        doi = (
            (density - min_) / (max_ - min_) if min_ != max_ else np.zeros_like(density)
        )

        return doi
