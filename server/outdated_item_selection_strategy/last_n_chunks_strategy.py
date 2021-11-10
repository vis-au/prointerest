from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from database import ID, get_from_processed

class LastNChunksStrategy(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that retrieves the last `n` chunks as outdated. All chunks
  older than `n` timesteps are consindered irrelevant.

  Properties
  ----------
  n_chunks : int
    The fixed (positive) number of chunks to be retrieved when checking for outdated items.
  '''
  def __init__(self, n_dims: int, n_chunks: int):
    super().__init__(n_dims)
    self.n_chunks = n_chunks

  def get_outdated_ids(self, current_chunk: int):
    res = get_from_processed([
      f"chunk > {current_chunk - self.n_chunks}"
    ], as_numpy=True)

    return res[ID.lower()]