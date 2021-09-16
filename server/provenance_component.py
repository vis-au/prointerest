from pandas.core.frame import DataFrame
from doi_component import *
import pandas as pd
import numpy as np

class ProvenanceComponent(DoiComponent):
  def __init__(self) -> None:
    super().__init__()
    self.weights = {}
    self.log = pd.DataFrame(np.empty((0, 3)), columns=["timestamp", "mode", "ids"])
    self.current_interest = pd.DataFrame(np.empty((0, 2)), columns=["id", "doi"])


  def add_interaction(self, interaction: list):
    as_df = pd.DataFrame([interaction], columns=["timestamp", "mode", "ids"])
    self.log = self.log.append(as_df, ignore_index=False)


  def get_values_for_ids(self, interacted_ids, X: DataFrame):
    return interacted_ids.merge(X.set_index("id"), on="id").drop(columns=["id"]).to_numpy()


  def train(self, X: DataFrame):
    interacted_ids = pd.DataFrame(X["id"].astype(np.int64))
    computed_doi = self.compute_doi(X)

    X["id"] = X["id"].astype(np.int64)
    training_data = interacted_ids.merge(X.set_index("id"), on="id").drop(columns=["id"]).to_numpy()
    training_labels = computed_doi.to_numpy()

    self.predictor.fit(training_data, training_labels)


  def evaluate_doi(self, X: DataFrame):
    # "flatten" the list of ids into separate rows
    s = self.log.set_index(['timestamp', "mode"])['ids']

    # create DataFrame, reshape by stack and convert MultiIndex to columns
    df = pd.DataFrame(s.values.tolist(), index=s.index).stack().reset_index()
    df.columns= ['timestamp', "mode",'i','id']

    # aggregate their count across the same interaction technique
    grouped_count = df.groupby(["mode", 'id']).size().reset_index(name='count')

    # aggregate the count for the same id
    total_count = grouped_count[["id", "count"]].groupby(["id"], as_index="id").aggregate("sum")

    # compute doi as relative frequency
    min_count = total_count["count"].min()
    max_count = total_count["count"].max()
    relative_count = (total_count["count"] - min_count) / (max_count - min_count)
    as_matrix = np.array([relative_count.index, relative_count]).transpose()
    as_df = pd.DataFrame(as_matrix, columns=["id", "doi"])
    as_df["id"] = as_df["id"].astype(np.int64)

    # get doi for ids in input
    ids = pd.DataFrame(X["id"].astype(np.int64), columns=["id"])
    doi = ids.set_index("id").join(as_df.set_index("id"), on="id", lsuffix="left_", rsuffix="right_")["doi"]

    # input might contain items that have not been interacted with, which evaluate to NaN, so set them 0
    doi.loc[doi.isna()] = 0

    return doi


  def predict_doi(self, X):
    X_ = X.drop(columns=["id"])
    return self.predictor.predict(X_.to_numpy())