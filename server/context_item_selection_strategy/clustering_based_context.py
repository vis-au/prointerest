from pandas import DataFrame
from sklearn.utils.random import sample_without_replacement
from sklearn.cluster import MiniBatchKMeans
from database import ID, CHUNK, get_from_processed
from storage_strategy.storage_strategy import StorageStrategy
from .context_item_selection_strategy import ContextItemSelectionStrategy


class ClusteringBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_clusters: int, n_samples_per_cluster: int) -> None:
        super().__init__(n_dims, storage)
        self.n_clusters = n_clusters
        self.n_samples_per_cluster = n_samples_per_cluster
        self.clustering = MiniBatchKMeans(n_clusters=self.n_clusters)

    def get_context_items(self, current_chunk: int):
        # get the latest chunk (use db because not in storage yet!)
        response = get_from_processed(
            [f"{CHUNK}={current_chunk-1}"],
            dimensions=ID,
            as_df=True
        )
        ids_list = response[ID.lower()].values.tolist()
        ids_list = list(map(str, ids_list))

        data = self.storage.get_items_for_ids(ids_list, as_df=True)
        numeric = data.select_dtypes(["number"]).to_numpy()
        # clustering = KMeans(n_clusters=self.n_clusters).fit(numeric)

        if len(numeric) == 0:
            return DataFrame()

        self.clustering.partial_fit(numeric)
        labels = self.clustering.labels_
        representatives = DataFrame()

        # sample a representative for every class
        for i in range(self.n_clusters):
            # determine how many items to pick from this cluster
            no_picks = min(self.n_samples_per_cluster, len(data[labels == i]))

            # if no item can be found in that class, skip
            if no_picks == 0:
                continue

            # pick the first elements in that class as a representative (could also pick randomly)
            picks = sample_without_replacement(len(data[labels == i]), no_picks)
            next_representatives = data[labels == i].iloc[picks]
            representatives = representatives.append(next_representatives)

        return representatives.reset_index(drop=True)
