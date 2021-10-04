from typing import final
import numpy as np
from database import *


class OutdatedItemSelectionStrategy:
  def __init__(self):
    pass

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
    response = self.get_outdated_ids(current_chunk)
    print(response)
    outdated_ids = response[ID.lower()].tolist()
    return get_items_for_ids(outdated_ids)


class NoChunkStrategy(OutdatedItemSelectionStrategy):
  '''' Outdated item detection strategy that never detects any outdated items.'''
  def get_outdated_ids(self, current_chunk: int):
    return get_from_processed([
      f"chunk = -1"
    ], as_numpy=True)


class LastNChunksStrategy(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that retrieves the last `n` chunks as outdated. All chunks
  old than `n` timesteps are consindered irrelevant.

  Properties
  ----------
  n_chunks : int
    The fixed (positive) number of chunks to be retrieved when checking for outdated items.
  '''
  def __init__(self, n_chunks: int):
    super().__init__()
    self.n_chunks = n_chunks

  def get_outdated_ids(self, current_chunk: int):
    return get_from_processed([
      f"chunk > {current_chunk - self.n_chunks}"
    ], as_numpy=True)


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
  def __init__(self, interval: int, max_age : int):
    super().__init__()
    self.interval = interval
    self.max_age = max_age

  def get_outdated_ids(self, current_chunk: int):
    return get_from_processed([
      f"MOD({CHUNK}, {current_chunk})=0",
      f"CHUNK < {self.max_age}"
    ], as_numpy=True)


class OutdatedBinStrategy(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that compares binnings before and after the computation of
  the doi value to determine items that are outdated, as their bin has changed significantly.
  '''
  def get_outdated_bins(self):
    return () # TODO: given bins before and after an update, find those that need updating.

  def get_outdated_ids(self, current_chunk: int):
    outdated = self.get_outdated_bins()
    return get_from_processed([
      f"{CHUNK} IN {str(tuple(outdated))}"
    ], as_numpy=True)