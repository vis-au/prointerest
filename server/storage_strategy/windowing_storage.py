import pandas as pd
from .storage_strategy import DF, ID, CHUNK, StorageStrategy


class WindowingStorage(StorageStrategy):
    def insert_chunk(self, chunk: pd.DataFrame, chunk_no: int):
        if len(self.storage) > 0 and self.storage.shape[1] != chunk.shape[1]:
            print("chunk does not match shape of data in storage. aborting ...")
            return

        self.storage = self.storage.append(chunk)
        self.storage.reset_index(drop=True, inplace=True)
        self.cursor.register(DF, self.storage)

        chunk_no_df = pd.DataFrame(chunk[ID])
        chunk_no_df[CHUNK] = chunk_no
        self.chunk_storage = self.chunk_storage.append(chunk_no_df)

        if len(self.storage) > self.max_size:
            self.out = self.storage[0: -self.max_size:]
            self.storage = self.storage[-self.max_size:]
            self.chunk_storage = self.chunk_storage[-self.max_size:]
        else:
            self.out = pd.DataFrame()
