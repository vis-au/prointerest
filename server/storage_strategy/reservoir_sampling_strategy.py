import pandas as pd
from numpy.random import randint, rand
from .storage_strategy import StorageStrategy

class ReservoirSamplingStrategy(StorageStrategy):
  def __init__(self, max_size) -> None:
      super().__init__(max_size)
      self.next_replacement = self.max_size
      self.processed = 0

  def reservoir_sample(self, chunk: pd.DataFrame):
    for i in range(len(chunk)):
      probability = rand()

      if probability < (len(chunk) / self.processed):
        replaces = randint(0, len(self.storage))
        self.storage.loc[replaces] = chunk.loc[i]

      self.processed += 1

  def insert_chunk(self, chunk: pd.DataFrame) -> None:
    if len(self.storage) > 0 and self.storage.shape[1] != chunk.shape[1]:
      return

    # if there is still space in the reservoir, add the entire/partial chunk
    if len(self.storage) + len(chunk) < self.max_size:
      self.storage = self.storage.append(chunk)
      self.processed += len(chunk)
    elif len(self.storage) < self.max_size:
      remaining_space = self.max_size - len(self.storage)
      remainder = chunk[-remaining_space:]
      self.storage = self.storage.append(remainder)
      rest = chunk[remaining_space:]
      self.processed = self.max_size
      self.reservoir_sample(rest)
    else:
      self.reservoir_sample(chunk)

    self.storage = self.storage.reset_index(drop=True)