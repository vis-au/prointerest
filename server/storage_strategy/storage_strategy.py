import duckdb
import numpy as np
import pandas as pd
from database import CHUNK, ID, get_dois

STORAGE_DB = "stored_db"


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

    def get_n_items_from_query(self, where_clause: str, n: int = None):
        if len(self.storage) == 0:
            return pd.DataFrame()

        # register if not already
        if not self.is_storage_registered and len(self.storage) > 0:
            self.cursor.register(STORAGE_DB, self.storage)
            self.is_storage_registered = True

        query = f"SELECT * FROM {STORAGE_DB} WHERE {where_clause}"

        # optionally limit the query to the first n items
        if n is not None:
            query += f" LIMIT {n}"

        response = self.cursor.execute(query)

        return response.fetchdf()

    def get_available_ids(self) -> pd.Series:
        if not self.is_storage_registered and len(self.storage) > 0:
            self.cursor.register(STORAGE_DB, self.storage)
            self.is_storage_registered = True
            return pd.Series()
        elif len(self.storage) == 0:
            return pd.Series()

        return self.storage[ID]

    def get_available_dois(self, with_ids=False) -> np.ndarray:
        available_ids = self.get_available_ids().tolist()
        available_dois = get_dois(available_ids)

        if with_ids:
            return np.array([available_ids, available_dois]).T
        else:
            return available_dois

    def get_available_chunks(self) -> np.ndarray:
        if len(self.chunk_storage) == 0:
            return np.empty(0)

        return self.chunk_storage[CHUNK].unique()

    def get_items_for_ids(self, ids: list, as_df=False):
        if not self.is_storage_registered and len(self.storage) > 0:
            self.cursor.register(STORAGE_DB, self.storage)
            self.is_storage_registered = True
            return pd.DataFrame()
        elif len(self.storage) == 0:
            return pd.DataFrame()

        response = self.cursor.execute(
            f"SELECT * FROM {STORAGE_DB} WHERE {ID} IN {tuple(ids)}"
        )

        return response.fetchdf() if as_df else response.fetchall()

    def get_items_for_chunks(self, chunks: list, as_df=False) -> pd.DataFrame:
        if len(chunks) == 0 or len(self.chunk_storage) == 0:
            return pd.DataFrame()

        ids_for_chunks = self.chunk_storage[self.chunk_storage[CHUNK].isin(chunks)]
        if len(ids_for_chunks) == 0:
            return pd.DataFrame()

        items_for_ids = self.storage[self.storage[ID].isin(ids_for_chunks[ID].tolist())]

        return items_for_ids if as_df else items_for_ids.to_numpy()

    def get_doi_for_ids(self, ids: list) -> np.ndarray:
        if len(ids) == 0:
            return np.empty(0)

        return get_dois(ids)

    def get_chunks_for_ids(self, ids: list) -> np.ndarray:
        if len(ids) == 0:
            return np.empty(0)

        return self.chunk_storage[self.chunk_storage[ID].isin(ids)][CHUNK].to_numpy()
