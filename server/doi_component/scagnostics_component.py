from pyscagnostics import scagnostics
import pandas as pd

from .doi_component import DoiComponent


SCAGNOSTICS = [
  "Outlying", "Skewed", "Clumpy", "Sparse", "Striated", "Convex", "Skinny", "Stringy", "Monotonic"
]
SCATTERPLOT_AXES: dict[str, str] = {
  "x": None,
  "y": None
}

class ScagnosticsComponent(DoiComponent):
  def __init__(self) -> None:
      super().__init__()
      self.weights = {
        "outlying": 0.11,
        "skewed": 0.11,
        "clumpy": 0.11,
        "sparse": 0.11,
        "striated": 0.11,
        "convex": 0.11,
        "skinny": 0.11,
        "stringy": 0.11,
        "monotonic": 0.11
      }

  def _compute_scagnostics(self, df):
    return scagnostics(df)


  def _get_mean_scangostics(self, result_generator):
      all_results = []
      for x, y, result in result_generator:
        measures, _ = result
        all_results += [measures]

      return pd.DataFrame(all_results).mean()


  def compute_doi(self, X: pd.DataFrame):
      X_ = X.drop(columns=["id"])

      # get scagnostics for the entire dataset
      results = scagnostics(X_)
      mean_all = self._get_mean_scangostics(results)

      # compute scagnostics without each item
      generators = X_.apply(lambda item: scagnostics(X_[X_.index != item.name]), axis=1)
      mean_per_item = generators.apply(self._get_mean_scangostics)

      total_doi = (mean_per_item - mean_all).mean(axis=1).abs()
      min_doi = total_doi.min()
      max_doi = total_doi.max()
      scaled_doi = (total_doi - min_doi) / (max_doi - min_doi)
      return scaled_doi