from pandas import DataFrame
from numpy import empty
from sklearn.cluster import KMeans
from database import ID, DOI_DB, PROCESSED_DB, get_from_data, get_from_processed
from .context_item_selection_strategy import ContextItemSelectionStrategy


class ClusteringBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, n_clusters: int) -> None:
        super().__init__(n_dims)
        self.n_clusters = n_clusters

    def get_context_items(self, current_chunk: int):
        data = get_from_data([f"{DOI_DB}.{ID} IN (SELECT {ID} FROM {PROCESSED_DB})"], as_df=True)
        numeric = data.select_dtypes(["number"]).to_numpy()
        clustering = KMeans(n_clusters=self.n_clusters).fit(numeric)

        labels = clustering.labels_
        representatives = []

        for i in range(self.n_clusters):
            # pick first element in that class as a representative (could also pick randomly)
            if len(data[labels == i]) == 0:
                e = DataFrame(empty((0, self.n_dims)))
                return e
            representatives += [data[labels == i].iloc[0]]

        return DataFrame(representatives)
