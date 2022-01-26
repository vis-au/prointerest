from outdated_item_selection_strategy.no_update import *
from outdated_item_selection_strategy.oldest_chunks_update import *
from outdated_item_selection_strategy.last_n_chunks_update import *
from outdated_item_selection_strategy.regular_interval_update import *
from outdated_item_selection_strategy.outdated_bin_update import *


def get_update_strategies(n_dims: int, n_chunks: int,
                          max_age: int) -> list[OutdatedItemSelectionStrategy]:
  return [
    ("no update", lambda: NoUpdate(
      n_dims=n_dims, storage=None
    )),
    ("oldest n chunks", lambda: OldestChunksUpdate(
      n_dims=n_dims, storage=None, max_age=max_age
    )),
    ("last n chunks", lambda: LastNChunksUpdate(
      n_dims=n_dims, n_chunks=n_chunks, storage=None
    )),
    ("regular intervals", lambda: RegularIntervalUpdate(
      n_dims=n_dims, n_chunks=n_chunks, storage=None, max_age=max_age
    )),
    # ("outdated bins", OutdatedBinUpdate(n_dims=n_dims, storage=None))
  ]
