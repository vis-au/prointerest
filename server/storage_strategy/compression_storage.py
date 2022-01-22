import pandas as pd
from numpy import append
from sklearn.cluster import KMeans
from .storage_strategy import DF, ID, CHUNK, StorageStrategy


class CompressionStorage(StorageStrategy):
    def __init__(self, max_size) -> None:
        super().__init__(max_size)
        self.kmeans = KMeans(n_clusters=self.max_size, random_state=0)

    def insert_chunk(self, chunk: pd.DataFrame, chunk_no: int) -> None:
        if len(self.storage) < self.max_size:
            self.storage = self.storage.append(chunk)
            return

        storage = self.storage.to_numpy()
        c = chunk.to_numpy()
        X = append(storage, c, axis=0)

        # compute clustering over all data currently in storage and the data from the chunk
        self.kmeans.fit(X)

        # the updated storage are the new cluster centers
        centers = self.kmeans.cluster_centers_
        self.storage = pd.DataFrame(centers)
        self.cursor.register(DF, self.storage)

        # update the chunk storage
        # FIXME: items in storage have no chunks, which means that using kmeans hinders some of the
        # chunk-based strategies. Use kmedoids instead:
        # https://scikit-learn-extra.readthedocs.io/en/stable/generated/sklearn_extra.cluster.KMedoids.html
        # self.chunk_storage
        # chunk_no_df[CHUNK] = chunk_no
        # self.chunk_storage = self.chunk_storage.append(chunk_no_df)
