from pandas import DataFrame
from numpy import empty
from sklearn.cluster import KMeans, MiniBatchKMeans
from database import ID, CHUNK, get_from_column_data, get_from_processed
from .context_item_selection_strategy import ContextItemSelectionStrategy


class ClusteringBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, n_clusters: int) -> None:
        super().__init__(n_dims)
        self.n_clusters = n_clusters
        self.clustering = MiniBatchKMeans(n_clusters=self.n_clusters)

    def get_context_items(self, current_chunk: int):
        response = get_from_processed(
            [f"{CHUNK}={current_chunk}"], dimensions=ID,
            as_df=True
        )
        ids_list = response[ID.lower()].values.tolist()
        ids_list = list(map(str, ids_list))
        ids_sql = ",".join(ids_list)

        data = get_from_column_data(
            [f"{ID} IN ({ids_sql})"],
            as_df=True
        )
        numeric = data.select_dtypes(["number"]).to_numpy()
        # clustering = KMeans(n_clusters=self.n_clusters).fit(numeric)
        self.clustering.partial_fit(numeric)

        labels = self.clustering.labels_
        representatives = []

        for i in range(self.n_clusters):
            # pick first element in that class as a representative (could also pick randomly)
            if len(data[labels == i]) == 0:
                e = DataFrame(empty((0, self.n_dims)))
                return e
            representatives += [data[labels == i].iloc[0]]

        return DataFrame(representatives)
