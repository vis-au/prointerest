from pandas.core.frame import DataFrame
from doi_component import *
import pandas as pd
import numpy as np

class ProvenanceComponent(DoiComponent):
  def __init__(self) -> None:
      super().__init__()
      self.weights = {}
      self.log = pd.DataFrame()
      self.log.columns = ["timestamp", "mode", "ids"]


  def train(self, X: DataFrame):
    trained_ids = self.current_interest.set_index("id").index.astype(np.float128)
    X["id"] = X["id"].astype(np.float128)
    training_data = trained_ids.merge(X, on="id").to_numy()
    training_labels = self.current_interest["doi"].to_numy()

    self.predictor.fit(training_data, training_labels)


  def evaluate_doi(self, X: DataFrame):
    # "flatten" the list of ids into separate rows
    s = self.log.set_index(['timestamp', "mode"])['ids']

    # create DataFrame, reshape by stack and convert MultiIndex to columns
    df = pd.DataFrame(s.values.tolist(), index=s.index).stack().reset_index()
    df.columns= ['timestamp', "mode",'i','id']

    # aggregate their count across the same interaction technique
    grouped_count = df.groupby(["mode", 'id']).size().reset_index(name='count')
    grouped_count

    # aggregate the count for the same id
    total_count = grouped_count[["id", "count"]].groupby(["id"]).aggregate("sum")
    total_count

    # compute doi as relative frequency
    min_count = total_count["count"].min()
    max_count = total_count["count"].max()
    relative_count = (total_count["count"] - min_count) / (max_count - min_count)
    as_matrix = np.array([relative_count.index, relative_count]).transpose()
    self.current_interest = pd.DataFrame(as_matrix, columns=["id", "doi"])

    self.current_interest["id"] = self.current_interest["id"].astype(np.float128)

    # return doi for ids in input
    ids = X["id"].astype(np.float128)
    return ids.merge(self.current_interest, on="id")


  def predict_doi(self, X):
    return self.predictor.predict(X.to_numy())