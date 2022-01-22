import pandas as pd
import numpy as np
import duckdb

from database import ID, CHUNK

DF = "stored_db"


class StorageStrategy:
    def __init__(self, max_size) -> None:
        self.max_size = max_size  # max number of items in storage
        self.storage = pd.DataFrame()  # current state of the storage
        self.chunk_storage = pd.DataFrame()  # chunks for ids in the current storage
        self.cursor = duckdb.connect()
        self.is_storage_registered = False

    def insert_chunk(self, chunk: pd.DataFrame, chunk_no: int = -1) -> None:
        return None

    def get_available_items(self) -> pd.DataFrame:
        return self.storage

    def get_available_ids(self) -> pd.Series:
        if not self.is_storage_registered and len(self.storage) > 0:
            self.cursor.register(DF, self.storage)
            self.is_storage_registered = True
            return pd.DataFrame()
        elif len(self.storage) == 0:
            print("nothing in storage")
            return pd.DataFrame()

        return self.storage[ID]

    def get_chunks_for_ids(self, ids: list[str]) -> np.ndarray:
        if len(ids) == 0:
            return np.empty(0)

        return self.chunk_storage[self.chunk_storage[ID].isin(ids)][CHUNK].to_numpy()

    def get_available_chunks(self) -> np.ndarray:
        if len(self.chunk_storage) == 0:
            return np.empty(0)

        return self.chunk_storage[CHUNK].unique()

    def get_items_for_ids(self, ids: list[str], as_df=False):
        if not self.is_storage_registered and len(self.storage) > 0:
            self.cursor.register(DF, self.storage)
            self.is_storage_registered = True
            return pd.DataFrame()
        elif len(self.storage) == 0:
            print("nothing in storage")
            return pd.DataFrame()

        response = self.cursor.execute(
            f"SELECT * FROM {DF} WHERE {ID} IN {tuple(ids)}"
        )

        return response.fetchdf() if as_df else response.fetchall()

    def get_items_for_chunks(self, chunks: list[str], as_df=False) -> pd.DataFrame:
        if len(chunks) == 0 or len(self.chunk_storage) == 0:
            return pd.DataFrame()

        ids_for_chunks = self.chunk_storage[self.chunk_storage[CHUNK].isin(chunks)]
        if len(ids_for_chunks) == 0:
            return pd.DataFrame()

        items_for_ids = self.storage[self.storage[ID].isin(ids_for_chunks[ID].tolist())]

        return items_for_ids if as_df else items_for_ids.to_numpy()
