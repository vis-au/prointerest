import numpy as np
import pandas as pd
from .doi_component import DoiComponent
from sklearn.metrics.pairwise import euclidean_distances


class AveragenessComponent(DoiComponent):
  def __init__(self, subspace=[]) -> None:
      super().__init__()
      self.subspace = subspace

  def compute_doi(self, X: pd.DataFrame):
    if len(X) == 0:
      return np.empty((0, ))
      # compute the median for each dimension in self.subsapce, then compute the euclidean distance

    X_ = X.select_dtypes(["number"]) if len(self.subspace) == 0 else X[self.subspace]
    X_median_item = np.array(X_.median()).reshape(1, -1)
    X_ = X_.to_numpy()

    distances = euclidean_distances(X_, X_median_item)
    min_distance = distances.min()
    max_distance = distances.max()

    if min_distance == max_distance:
      return np.zeros((len(X), ))

    # normalize distances
    doi = (distances - min_distance) / (max_distance - min_distance)
    doi = doi.reshape(-1, )

    return doi





