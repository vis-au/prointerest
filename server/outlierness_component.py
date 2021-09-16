from doi_component import DoiComponent
import pandas as pd
import numpy as np

from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

# adapted from https://scikit-learn.org/stable/modules/outlier_detection.html
class OutliernessComponent(DoiComponent):
  def __init__(self) -> None:
    super().__init__()
    self.outliers_fraction = 0.15
    self.outlierness_measures = self.generate_measures()
    self.current_interest: pd.DataFrame = None


  def generate_measures(self):
    return [
      EllipticEnvelope(contamination=self.outliers_fraction),
      svm.OneClassSVM(nu=self.outliers_fraction, kernel="rbf", gamma=0.1),
      IsolationForest(contamination=self.outliers_fraction, random_state=0),
      # LocalOutlierFactor(n_neighbors=35, contamination=self.outliers_fraction)
    ]


  def compute_doi(self, X: pd.DataFrame):
    X_ = X.to_numpy()
    predictions = np.array(
      [measure.fit(X_).predict(X_) for measure in self.outlierness_measures]
    )
    sum = predictions.sum(axis=0)
    scaled = sum / len(predictions)

    return scaled