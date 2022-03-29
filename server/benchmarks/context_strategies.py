from typing import Callable, List, Tuple

from context_item_selection_strategy.no_context import *
from context_item_selection_strategy.chunk_based_context import *
from context_item_selection_strategy.sampling_based_context import *
from context_item_selection_strategy.clustering_based_context import *
from context_item_selection_strategy.doi_based_context import *


CONTEXT_STRATEGY_LABELS = [
  "no context",
  "random chunk based",
  "most recent chunk based",
  "sampling based",
  "clustering based",
  "doi based"
]


def get_context_strategies(n_dims: int, n_chunks: int, n_bins: int) -> List[Tuple[str, Callable[[], ContextItemSelectionStrategy]]]:
  return list(
    map(
      lambda label: (label, lambda: get_context_strategy(label, n_dims, n_chunks, n_bins)),
      CONTEXT_STRATEGY_LABELS
    )
  )


def get_context_strategy(label: str, n_dims: int, n_chunks: int, n_bins: int) -> ContextItemSelectionStrategy:
  if label == "no context":
    return NoContext(n_dims=n_dims, storage=None)
  elif label == "random chunk based":
    return RandomChunkBasedContext(n_dims=n_dims, n_chunks=n_chunks, storage=None)
  elif label == "most recent chunk based":
    return MostRecentChunkBasedContext(n_dims=n_dims, n_chunks=n_chunks, storage=None)
  elif label == "sampling based":
    return RandomSamplingBasedContext(n_dims=n_dims, storage=None)
  elif label == "clustering based":
    return ClusteringBasedContext(n_dims=n_dims, n_clusters=n_bins, storage=None)
  elif label == "doi based":
    return DoiBasedContext(n_dims=n_dims, n_bins=n_bins, storage=None)
