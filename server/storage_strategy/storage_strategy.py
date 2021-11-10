import pandas as pd

class StorageStrategy:
  def __init__(self, max_size) -> None:
    self.max_size = max_size
    self.storage = pd.DataFrame()
    self.out = pd.DataFrame()

  def insert_chunk(self, chunk: pd.DataFrame) -> None:
    return None

  def get_storage(self) -> pd.DataFrame:
    return self.storage

  def get_out(self) -> pd.DataFrame:
    return self.out