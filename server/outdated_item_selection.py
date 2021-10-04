from typing import final
import numpy as np
from database import *


class OutdatedItemSelectionStrategy:
  def __init__(self):
    pass

  def get_outdated_ids(self, current_chunk: int) -> np.ndarray:
    return np.array([])

  @final
  def get_outdated_items(self, current_chunk: int) -> np.ndarray:
    response = self.get_outdated_ids(current_chunk)
    print(response)
    outdated_ids = response[ID.lower()].tolist()
    return get_items_for_ids(outdated_ids)


class NoChunkStrategy(OutdatedItemSelectionStrategy):
  def get_outdated_ids(self, current_chunk: int):
    return get_from_processed([
      f"chunk = -1"
    ], as_numpy=True)


class LastNChunksStrategy(OutdatedItemSelectionStrategy):
  def __init__(self, n_chunks: int):
    super().__init__()
    self.n_chunks = n_chunks

  def get_outdated_ids(self, current_chunk: int):
    return get_from_processed([
      f"chunk > {current_chunk - self.n_chunks}"
    ], as_numpy=True)


class RegularIntervalStrategy(OutdatedItemSelectionStrategy):
  def __init__(self, interval: int, max_age : int):
    super().__init__()
    self.interval = interval
    self.max_age = max_age

  def get_outdated_ids(self, current_chunk: int):
    return get_from_processed([
      f"MOD({CHUNK}, {current_chunk})=0"
    ], as_numpy=True)


class OutdatedBinStrategy(OutdatedItemSelectionStrategy):
  def get_outdated_bins(self):
    return () # TODO: given bins before and after an update, find those that need updating.

  def get_outdated_ids(self, current_chunk: int):
    outdated = self.get_outdated_bins()
    return get_from_processed([
      f"{CHUNK} IN {str(tuple(outdated))}"
    ], as_numpy=True)