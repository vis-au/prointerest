import pandas as pd
from numpy import append
from sklearn.cluster import KMeans
from .storage_strategy import StorageStrategy


class CompressionStrategy(StorageStrategy):
    def __init__(self, max_size) -> None:
        super().__init__(max_size)
        self.kmeans = KMeans(n_clusters=self.max_size, random_state=0)

    def insert_chunk(self, chunk: pd.DataFrame) -> None:
        if len(self.storage) < self.max_size:
            self.storage = self.storage.append(chunk)
            return

        storage = self.storage.to_numpy()
        c = chunk.to_numpy()
        X = append(storage, c, axis=0)

        self.kmeans.fit(X)

        centers = self.kmeans.cluster_centers_
        self.storage = pd.DataFrame(centers)
