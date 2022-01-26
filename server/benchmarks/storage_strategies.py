from storage_strategy.no_storage import *
from storage_strategy.compression_storage import *
from storage_strategy.progressive_bin_sampler import *
from storage_strategy.reservoir_sampling_storage import *
from storage_strategy.windowing_storage import *


def get_storage_strategies(storage_size: int) -> list[StorageStrategy]:
  return [
    ("no_storage_strategy", NoStorage()),
    ("compression_strategy", CompressionStorage(max_size=storage_size)),
    ("progressive_bin_sampler", ProgressiveBinSampler()),
    ("reservoir_sampling_strategy", ReservoirSamplingStorage(max_size=storage_size)),
    ("windowing_strategy", WindowingStorage(max_size=storage_size))
  ]
