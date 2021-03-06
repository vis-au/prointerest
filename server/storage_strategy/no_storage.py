from .storage_strategy import StorageStrategy
from database import get_items_for_ids


class NoStorage(StorageStrategy):
  def __init__(self) -> None:
      super().__init__(-1)

  def get_items_for_ids(self, ids: list, as_df=False):
      # no items are "cached", instead uses the full dataset (slow!)
      return get_items_for_ids(ids, as_df)
