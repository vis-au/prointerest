import numpy as np

from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from database import ID, CHUNK, get_from_latest_update

class OldestChunksStrategy(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that always returns those items that have been processed
  the longest ago.

  Properties
  ----------
  n_chunks : int
    The fixed (positive) number of chunks to be retrieved when checking for outdated items.

  max_age : int
    The number of latest chunks that should be considered when checking for outdated items. "Latest"
    here refers to the first time a chunk was processed.
  '''
  def __init__(self, n_dims: int, n_chunks: int, max_age: int):
    super().__init__(n_dims)
    self.n_chunks = n_chunks
    self.max_age = max_age

  def get_outdated_ids(self, current_chunk: int):
    ages = get_from_latest_update(["TRUE"], dimensions=CHUNK, distinct=True, as_df=True)
    oldest = min(ages[CHUNK.lower()].to_numpy())
    outdated_ids = get_from_latest_update([f"{CHUNK}={oldest}"], dimensions=ID, as_df=True)
    print(f"oldest chunk is {oldest}")
    return outdated_ids[ID.lower()].to_numpy()