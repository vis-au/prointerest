from pandas import DataFrame
from sklearn.utils.random import sample_without_replacement
from sklearn.cluster import MiniBatchKMeans
from storage_strategy.storage_strategy import StorageStrategy
from .context_item_selection_strategy import ContextItemSelectionStrategy


class ClusteringBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_clusters: int) -> None:
        super().__init__(n_dims, storage)
        self.n_clusters = n_clusters
        self.clustering = MiniBatchKMeans(n_clusters=self.n_clusters)

    def __train_clustering(self, current_chunk: int):
        # get the latest chunk (must use db because not in storage yet!)
        most_recent_items = self.storage.get_items_for_chunks([current_chunk - 1], as_df=True)
        most_recent_items = most_recent_items.select_dtypes(["number"]).to_numpy()
        # clustering = KMeans(n_clusters=self.n_clusters).fit(numeric)

        # did not find anything to train the model with (storage still empty @chunk=0 and 1)
        if len(most_recent_items) == 0:
            return False

        # incrementally train the clustering on the newest data
        self.clustering.partial_fit(most_recent_items)
        return True

    def get_context_items(self, n: int, current_chunk: int):
        has_trained_clustering = self.__train_clustering(current_chunk)
        if not has_trained_clustering:
            return DataFrame()

        # use the new model to predict the labels for all items in storage
        stored_items = self.storage.get_available_items()
        numeric_stored_data = stored_items.select_dtypes(["number"]).to_numpy()
        labels = self.clustering.predict(numeric_stored_data)

        representatives = DataFrame()
        n_samples_per_cluster = n // self.n_clusters

        # sample representatives from  class
        for i in range(self.n_clusters):
            # determine how many items to pick from this cluster
            n_picks = min(n_samples_per_cluster, len(stored_items[labels == i]))

            # if no item can be found in that class, skip
            if n_picks == 0:
                continue

            picks = sample_without_replacement(len(stored_items[labels == i]), n_picks)
            next_representatives = stored_items[labels == i].iloc[picks]
            representatives = representatives.append(next_representatives)

        return representatives.reset_index(drop=True)
