from numpy import empty
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy
from database import ID, TIMESTAMP, get_from_latest_update


class OldestChunksUpdate(OutdatedItemSelectionStrategy):
    """Outdated item detection strategy that always returns those items that have been processed
    the longest ago.

    Properties
    ----------
    max_age : int
      The number of latest chunks that should be considered when checking for outdated items.
      "Latest" here refers to the chunk number time a chunk was initially processed.
    """

    def __init__(self, n_dims: int, storage: StorageStrategy, max_age: int):
        super().__init__(n_dims, storage)
        self.max_age = max_age

    def get_outdated_ids(self, n: int, current_chunk: int):
        # get all available ids from storage
        all_ids = self.storage.get_available_ids()
        if len(all_ids) == 0:
            return empty((0, self.n_dims))

        all_ids = all_ids.to_list()
        if len(all_ids) == 1:
            all_ids += all_ids

        # get all timestaps available in the database
        response = get_from_latest_update(
            [f"{ID} IN {tuple(all_ids)} ORDER BY {TIMESTAMP}"], as_df=True
        )

        # find all chunks that belong to those timestamps (MIGHT BE MORE THAN n!)
        # since the data comes back in order, we can just take the last n (except latest)
        outdated_ids = response[ID.lower()].iloc[-n:]

        if len(outdated_ids) == 0:
            return empty((0, self.n_dims))

        return outdated_ids
