from context_item_selection_strategy.no_context import *
from context_item_selection_strategy.chunk_based_context import *
from context_item_selection_strategy.sampling_based_context import *
from context_item_selection_strategy.clustering_based_context import *
from context_item_selection_strategy.doi_based_context import *


def get_context_strategies(n_dims: int, n_chunks: int, n_bins: int):
  return [
    ("no context", lambda: NoContext(
      n_dims=n_dims, storage=None
    )),
    ("random chunk based", lambda: RandomChunkBasedContext(
      n_dims=n_dims, n_chunks=n_chunks, storage=None
    )),
    ("most recent chunk based", lambda: MostRecentChunkBasedContext(
      n_dims=n_dims, n_chunks=n_chunks, storage=None
    )),
    ("sampling based", lambda: RandomSamplingBasedContext(
      n_dims=n_dims, storage=None
    )),
    ("clustering based", lambda: ClusteringBasedContext(
      n_dims=n_dims, n_clusters=n_bins, storage=None
    )),
    ("doi based", lambda: DoiBasedContext(
      n_dims=n_dims, n_bins=n_bins, storage=None
    )),
  ]
