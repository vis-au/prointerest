from pandas import DataFrame
from numpy import array
from sklearn.cluster import KMeans
from database import get_from_data
from .context_item_selection_strategy import ContextItemSelectionStrategy

class ClusteringBasedContext(ContextItemSelectionStrategy):
  def __init__(self, n_dims: int, n_clusters: int) -> None:
    super().__init__(n_dims)
    self.n_clusters = n_clusters


  def get_context_items(self, current_chunk: int):
    data = get_from_data(["TRUE"], as_df=True)
    numeric = DataFrame(data).select_dtypes(["number"]).to_numpy()
    clustering = KMeans(n_clusters=self.n_clusters).fit(numeric)

    labels = clustering.labels_
    representatives = []

    for i in range(self.n_clusters):
      representatives += [data[labels == i].to_numpy()[0]]

    return array(representatives)

