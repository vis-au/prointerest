import numpy as np
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from database import ID, CHUNK, get_from_processed

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
    self.chunk_ages = np.empty(0)
    self.max_age = max_age

  def get_outdated_ids(self, current_chunk: int):
    if len(self.chunk_ages) > self.max_age:
      oldest_chunk_index = np.argmax(self.chunk_ages[-self.max_age:])
      oldest_chunk_index += len(self.chunk_ages) - self.max_age
    else:
      oldest_chunk_index = np.argmax(self.chunk_ages)

    self.chunk_ages[oldest_chunk_index] = 0

    res = get_from_processed([
      f"{CHUNK}={oldest_chunk_index}"
    ], as_numpy=True)

    return res[ID.lower()]