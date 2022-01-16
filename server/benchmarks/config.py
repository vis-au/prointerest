from doi_component.outlierness_component import OutliernessComponent

from database import initialize_db, drop_tables

from storage_strategy.no_storage_strategy import *
from storage_strategy.compression_strategy import *
from storage_strategy.progressive_bin_sampler import *
from storage_strategy.reservoir_sampling_strategy import *
from storage_strategy.windowing_strategy import *

from outdated_item_selection_strategy.no_update import *
from outdated_item_selection_strategy.oldest_chunks_update import *
from outdated_item_selection_strategy.last_n_chunks_update import *
from outdated_item_selection_strategy.regular_interval_update import *
from outdated_item_selection_strategy.outdated_bin_update import *

from context_item_selection_strategy.no_context import *
from context_item_selection_strategy.chunk_based_context import *
from context_item_selection_strategy.sampling_based_context import *
from context_item_selection_strategy.clustering_based_context import *


def reset():
  drop_tables()
  initialize_db(data_path, column_data_path)


outlierness = OutliernessComponent(["ratio", "duration"])

total_size = 100000  # total number of processed items, not nec. the size of the data
chunk_size = 1000  # number of new items retrieved per step
chunks = round(total_size / chunk_size)  # number of steps
max_size = chunk_size * 5  # maximum size of storages

data_path = "../data/nyc_taxis.shuffled_full.csv.gz"
column_data_path = "../data/nyc_taxis.shuffled_full.parquet"
n_dims = 17  # number of dimensions in the data


storage_strategies = [
  ("no_storage_strategy", NoStorageStrategy()),
  ("compression_strategy", CompressionStrategy(max_size=max_size)),
  ("progressive_bin_sampler", ProgressiveBinSampler()),
  ("reservoir_sampling_strategy", ReservoirSamplingStrategy(max_size=max_size)),
  ("windowing_strateg", WindowingStrategy(max_size=max_size))
]

update_strategies = [
  ("no chunk", NoUpdate(n_dims=n_dims, storage=None)),
  ("oldest n chunks", OldestChunksUpdate(n_dims=n_dims, storage=None, n_chunks=3, max_age=10)),
  ("last n chunks", LastNChunksUpdate(n_dims=n_dims, storage=None, n_chunks=3)),
  ("regular intervals", RegularIntervalUpdate(n_dims=n_dims, storage=None, interval=2, max_age=10)),
  ("outdated bins", OutdatedBinUpdate(n_dims=n_dims, storage=None))
]

context_strategies = [
  ("no context", NoContext(n_dims=n_dims, storage=None)),
  ("chunk based", RandomChunkBasedContext(n_dims=n_dims, n_chunks=3, storage=None)),
  ("sampling based", RandomSamplingBasedContext(n_dims=n_dims, n_samples=chunk_size, storage=None)),
  ("clustering based", ClusteringBasedContext(n_dims=n_dims, n_clusters=chunk_size, storage=None))
]
