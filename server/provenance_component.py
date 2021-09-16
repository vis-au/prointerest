from pandas.core.frame import DataFrame
from doi_component import *
import pandas as pd
import numpy as np

class ProvenanceComponent(DoiComponent):
  def __init__(self) -> None:
    super().__init__()
    self.weights = {}
    self.log = pd.DataFrame(np.empty((0, 3)), columns=["timestamp", "mode", "ids"])
    self.log = self.log.set_index("timestamp")
    self.current_interest = pd.DataFrame(np.empty((0, 2)), columns=["id", "doi"])
    self.current_interest = self.current_interest.set_index("id")


  def add_interaction(self, interaction: list):
    as_df = pd.DataFrame([interaction], columns=["timestamp", "mode", "ids"])
    self.log = self.log.append(as_df, ignore_index=False)


  def get_values_for_ids(self, interacted_ids, X: DataFrame):
    return interacted_ids.merge(X.set_index("id"), on="id").drop(columns=["id"]).to_numpy()


  def train(self, X: DataFrame):
    interacted_ids = pd.DataFrame(self.current_interest["id"].astype(np.int64))
    interacted_dois = pd.DataFrame(self.current_interest["doi"])

    X["id"] = X["id"].astype(np.int64)
    training_data = self.get_values_for_ids(interacted_ids, X)
    training_labels = interacted_dois.to_numpy()

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

    self.current_interest["id"] = self.current_interest["id"].astype(np.int64)

    # return doi for ids in input
    ids = pd.DataFrame(X["id"].astype(np.int64), columns=["id"])
    return ids.merge(self.current_interest, on="id")


  def predict_doi(self, X):
    return self.predictor.predict(X.to_numy())