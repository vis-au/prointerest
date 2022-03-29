from typing import Callable, List, Tuple

from outdated_item_selection_strategy.no_update import *
from outdated_item_selection_strategy.oldest_chunks_update import *
from outdated_item_selection_strategy.last_n_chunks_update import *
from outdated_item_selection_strategy.regular_interval_update import *
from outdated_item_selection_strategy.binned_update import *

UPDATE_STRATEGY_LABELS = [
  "no update",
  "oldest n chunks",
  "last n chunks",
  "regular intervals",
  "outdated bins"
]


def get_update_strategies(n_dims: int, n_chunks: int, max_age: int, n_bins: int) -> List[Tuple[str, Callable[[], OutdatedItemSelectionStrategy]]]:
  return list(
    map(
      lambda label: (label, lambda: get_update_strategy(label, n_dims, n_chunks, max_age, n_bins)),
      UPDATE_STRATEGY_LABELS
    )
  )


def get_update_strategy(label: str, n_dims: int, n_chunks: int, max_age: int, n_bins: int) -> OutdatedItemSelectionStrategy:
  if label == "no update":
    return NoUpdate(n_dims=n_dims, storage=None)
  elif label == "oldest n chunks":
    return OldestChunksUpdate(n_dims=n_dims, storage=None, max_age=max_age)
  elif label == "last n chunks":
    return LastNChunksUpdate(n_dims=n_dims, n_chunks=n_chunks, storage=None)
  elif label == "regular intervals":
    return RegularIntervalUpdate(n_dims=n_dims, n_chunks=n_chunks, storage=None, max_age=max_age)
  elif label == "outdated bins":
    return BinnedUpdate(n_dims=n_dims, storage=None, n_bins=n_bins)
