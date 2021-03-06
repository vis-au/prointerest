from typing import Callable, List, Tuple

from storage_strategy.no_storage import *
from storage_strategy.compression_storage import *
from storage_strategy.progressive_bin_sampler import *
from storage_strategy.reservoir_sampling_storage import *
from storage_strategy.windowing_storage import *

STORAGE_STRATEGY_LABELS = [
  "no storage",
  "compression",
  # "bin sampling",
  "reservoir",
  "windowing"
]


def get_storage_strategies(storage_size: int) -> List[Tuple[str, Callable[[], StorageStrategy]]]:
  return list(
    map(
      lambda label: (label, lambda: get_storage_strategy(label, storage_size)),
      STORAGE_STRATEGY_LABELS
    )
  )


def get_storage_strategy(label: str, max_size: int) -> StorageStrategy:
  if label == "no storage":
    return NoStorage()
  elif label == "compression":
    return CompressionStorage(max_size=max_size)
  elif label == "bin sampling":
    return ProgressiveBinSampler()
  elif label == "reservoir":
    return ReservoirSamplingStorage(max_size=max_size)
  elif label == "windowing":
    return WindowingStorage(max_size=max_size)
