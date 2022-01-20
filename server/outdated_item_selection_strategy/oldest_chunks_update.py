from numpy import empty
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
        # get all available ids from storage
        all_ids = self.storage.get_available_ids()
        if len(all_ids) == 0:
          return empty((0, self.n_dims))

        all_ids = all_ids.to_list()
        if len(all_ids) == 1:
          all_ids += all_ids

        # get all timestaps available in the database
        response = get_from_latest_update(
            [
              f"{ID} IN {tuple(all_ids)} ORDER BY {TIMESTAMP}"
            ],
            as_df=True
        )

        # find all chunks that belong to those timestamps (might be more than n_chunks!)
        # since the data comes back in order, we can just take the last n_chunks (except latest)
        oldest_timestamps = response[TIMESTAMP].unique()[-self.n_chunks:-1]
        oldest_timestamps_ids = response[response[TIMESTAMP].isin(oldest_timestamps)][ID.lower()]
        oldest_ts_ids_list = oldest_timestamps_ids.tolist()

        oldest_timestamps_chunks = self.storage.get_chunks_for_ids(oldest_ts_ids_list).tolist()
        outdated_items = self.storage.get_items_for_chunks(
          oldest_timestamps_chunks[-self.n_chunks:],
          as_df=True
        )
        if len(outdated_items) == 0:
          return empty((0, self.n_dims))
        outdated_ids = outdated_items[ID]
        return outdated_ids
