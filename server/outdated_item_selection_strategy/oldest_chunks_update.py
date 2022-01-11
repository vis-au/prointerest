from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy
from database import ID, TIMESTAMP, get_from_latest_update


class OldestChunksUpdate(OutdatedItemSelectionStrategy):
    """Outdated item detection strategy that always returns those items that have been processed
    the longest ago.

    Properties
    ----------
    n_chunks : int
      The fixed (positive) number of chunks to be retrieved when checking for outdated items.

    max_age : int
      The number of latest chunks that should be considered when checking for outdated items. "Latest"
      here refers to the first time a chunk was processed.
    """

    def __init__(self, n_dims: int, storage: StorageStrategy, n_chunks: int, max_age: int):
        super().__init__(n_dims, storage)
        self.n_chunks = n_chunks
        self.max_age = max_age

    def get_outdated_ids(self, current_chunk: int):
        response = get_from_latest_update(
            ["TRUE"], dimensions=f"MIN({TIMESTAMP})", distinct=True, as_df=True
        )
        oldest = response[f"min({TIMESTAMP.lower()})"].to_numpy()[0]
        outdated_ids = get_from_latest_update(
            [f"{TIMESTAMP}='{oldest}'"], dimensions=ID, as_df=True
        )
        return outdated_ids[ID.lower()].to_numpy()
