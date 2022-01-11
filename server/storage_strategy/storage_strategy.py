import pandas as pd
import duckdb

from database import ID

DF = "stored_db"


class StorageStrategy:
    def __init__(self, max_size) -> None:
        self.max_size = max_size  # max number of items in storage
        self.storage = pd.DataFrame()  # current state of the storage
        self.cursor = duckdb.connect()
        self.is_storage_registered = False

    def insert_chunk(self, chunk: pd.DataFrame) -> None:
        return None

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
