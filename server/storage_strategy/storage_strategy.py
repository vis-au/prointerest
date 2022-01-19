import pandas as pd
import numpy as np
import duckdb

from database import ID, CHUNK, get_from_processed

DF = "stored_db"


class StorageStrategy:
    def __init__(self, max_size) -> None:
        self.max_size = max_size  # max number of items in storage
        self.storage = pd.DataFrame()  # current state of the storage
        self.cursor = duckdb.connect()
        self.is_storage_registered = False

    def insert_chunk(self, chunk: pd.DataFrame) -> None:
        return None

    def get_available_ids(self) -> pd.Series:
        if not self.is_storage_registered:
            return pd.Series()

        return self.storage[ID]

    def get_available_chunks(self) -> np.ndarray:
        ids = self.get_available_ids().to_numpy()

        if len(ids) == 0:
            return pd.DataFrame()
        elif len(ids) == 1:
            ids += ids

        ids_sql = tuple(ids)

        chunks_for_ids = get_from_processed(
            [f"{ID} IN {ids_sql}"],
            dimensions=f"{CHUNK}",
            distinct=True,
            as_df=True
        )
        chunks = chunks_for_ids[CHUNK.lower()].to_numpy().reshape(-1,)
        return chunks

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

    def get_items_for_chunks(self, chunks: list[str], as_df=False):
        if len(chunks) == 0:
            return pd.DataFrame()

        if len(chunks) == 1:
            chunks += chunks

        ids_for_chunks = get_from_processed([f"{CHUNK} in {tuple(chunks)}"], as_df=True)[ID.lower()]
        ids_for_chunks = ids_for_chunks.to_list()
        ids_for_chunks = list(map(str, ids_for_chunks))
        return self.get_items_for_ids(ids_for_chunks, as_df=as_df)
