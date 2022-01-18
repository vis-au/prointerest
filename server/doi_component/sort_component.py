import pandas as pd
import numpy as np
from .doi_component import DoiComponent


class SortComponent(DoiComponent):
  def __init__(self, sort_column: str) -> None:
      super().__init__()
      self.sort_column = sort_column

  def compute_doi(self, X: pd.DataFrame):
    if len(X) == 0:
      return np.empty((0, ))

    # order = np.argsort(X.select_dtypes(["number"]), axis=0)
    # order = order.sum(axis=1)
    order = np.argsort(X[self.sort_column], axis=0)
    doi = (order - order.min()) / (order.max() - order.min())

    return np.array(doi).reshape(len(X), )
