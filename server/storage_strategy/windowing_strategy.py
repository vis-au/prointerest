import pandas as pd
from .storage_strategy import StorageStrategy

class WindowingStrategy(StorageStrategy):
  def insert_chunk(self, chunk: pd.DataFrame):
    if len(self.storage) > 0 and self.storage.shape[1] != chunk.shape[1]:
      return

    self.storage = self.storage.append(chunk)

    if len(self.storage) > self.max_size:
      self.out = self.storage[0:-self.max_size:]
      self.storage = self.storage[-self.max_size:]
    else:
      self.out = pd.DataFrame()