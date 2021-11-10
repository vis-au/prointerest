from typing import final
import numpy as np
from database import *


class OutdatedItemSelectionStrategy:
  def __init__(self, n_dims: int):
    self.n_dims = n_dims

  def get_outdated_ids(self, current_chunk: int) -> np.ndarray:
    ''' This function is to be overwritten by the particular subclass strategy. It computes the
    `ids` of items that are outdated, based on some heuristic.

    Returns an ndarray of shape (n, ).'''
    return np.empty((0, ))

  @final
  def get_outdated_items(self, current_chunk: int) -> np.ndarray:
    ''' Takes the `ids` of items computed in `get_outdated_ids` and retrieves the actual data from
    the database. Returns an ndarray of shape (n, m).

    Parameters
    ----------
    current_chunk : int
      The index of the current chunk.
    '''
    outdated_ids = self.get_outdated_ids(current_chunk)
    if len(outdated_ids) == 0:
      return np.empty((0, self.n_dims))
    outdated_id_list = outdated_ids.tolist()
    return get_items_for_ids(outdated_id_list)


class NoChunkStrategy(OutdatedItemSelectionStrategy):
  '''' Outdated item detection strategy that never detects any outdated items.'''
  def get_outdated_ids(self, current_chunk: int):
    res = get_from_processed(["FALSE"], as_numpy=True)

    return res[ID.lower()]


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


class RegularIntervalStrategy(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that retrieves items in regular intervals, such that an item
  becomes outdated every `interval` steps.

  This strategy is presumably the most costly, as the number of outdated chunks grows linearly with
  each processed chunk. To overcome this, the `max_age` property allows to define a maximum age,
  after which older chunks will no longer be considered.

  Properties
  ----------
  interval : int
    The interval in which chunks should be recomputed.
  max_age : int
    The maximum age of considered chunks, thus the lower `max_age`, the faster the retrieval.
  '''
  def __init__(self, n_dims: int, interval: int, max_age : int):
    super().__init__(n_dims)
    self.interval = interval
    self.max_age = max_age

  def get_outdated_ids(self, current_chunk: int):
    res = get_from_processed([
      f"MOD({CHUNK}, {current_chunk})=0",
      f"CHUNK < {self.max_age}"
    ], as_numpy=True)

    return res[ID.lower()]


class OutdatedBinStrategy(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that compares binnings before and after the computation of
  the doi value to determine items that are outdated, as their bin has changed significantly.
  '''
  def get_outdated_bins(self):
    return () # TODO: given bins before and after an update, find those that need updating.

  def get_outdated_ids(self, current_chunk: int):
    outdated = self.get_outdated_bins()
    if len(outdated) == 0:
      return np.empty((0,))
    res = get_from_processed([
      f"{CHUNK} IN {str(tuple(outdated))}"
    ], as_numpy=True)

    return res[ID.lower()]