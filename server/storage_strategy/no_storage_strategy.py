import pandas as pd
from .storage_strategy import StorageStrategy
from database import ID, get_from_processed, get_items_for_ids


class NoStorageStrategy(StorageStrategy):
  def __init__(self) -> None:
      super().__init__(-1)

  def insert_chunk(self, chunk: pd.DataFrame):
      return

  def get_storage(self) -> pd.DataFrame:
      processed_ids = get_from_processed(["TRUE"], dimensions=ID, as_df=True)[ID.lower()].to_list()
      storage = get_items_for_ids(processed_ids, as_df=True)

      return storage
