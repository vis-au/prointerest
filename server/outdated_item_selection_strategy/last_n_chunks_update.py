from numpy import empty
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy
from database import ID


class LastNChunksUpdate(OutdatedItemSelectionStrategy):
    """Outdated item detection strategy that retrieves the last `n` chunks as outdated. All chunks
    older than `n` timesteps are consindered irrelevant.

    Properties
    ----------
    n_chunks : int
      The fixed (positive) number of chunks to be retrieved when checking for outdated items.
    """

    def __init__(self, storage: StorageStrategy, n_dims: int, n_chunks: int):
        super().__init__(n_dims, storage)
        self.n_chunks = n_chunks

    def get_outdated_ids(self, current_chunk: int):
        self.storage.get_available_chunks()
        last_n_chunks = list(range(current_chunk, current_chunk - self.n_chunks))
        outdated_items = self.storage.get_items_for_chunks(last_n_chunks, as_df=True)

        if len(outdated_items) == 0:
            return empty((0, self.n_dims))

        outdated_ids = outdated_items[ID]

        return outdated_ids
