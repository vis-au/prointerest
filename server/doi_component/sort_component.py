import pandas as pd
import numpy as np
from .doi_component import DoiComponent


class SortComponent(DoiComponent):
  def __init__(self, sort_columns: list[str]) -> None:
      super().__init__()
      self.sort_columns = sort_columns

  def compute_doi(self, X: pd.DataFrame):
    if len(X) == 0:
      return np.empty((0, ))

    # get positions in sorted column per sort_column
    sorted_X = np.argsort(X[self.sort_columns], axis=0)
    # sum all positions in sorted columns
    summed_X = sorted_X.sum(axis=1)
    # scale to [0, 1]
    doi = summed_X / (len(summed_X) * len(self.sort_columns))

    return np.array(doi).reshape(len(X), )
