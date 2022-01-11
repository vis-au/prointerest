import pandas as pd


class StorageStrategy:
    def __init__(self, max_size) -> None:
        self.max_size = max_size  # max number of items in storage
        self.storage = pd.DataFrame()  # current state of the storage
        self.out = pd.DataFrame()  # data that was discarded from storage last

    def insert_chunk(self, chunk: pd.DataFrame) -> None:
        return None

    def get_storage(self) -> pd.DataFrame:
        return self.storage

    def get_out(self) -> pd.DataFrame:
        return self.out
