from numpy import empty
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy
from database import ID


class RegularIntervalUpdate(OutdatedItemSelectionStrategy):
    """Outdated item detection strategy that retrieves items in regular intervals, such that an item
    becomes outdated every `interval` steps.

    This strategy is presumably the most costly, as the number of outdated chunks grows linearly
    with each processed chunk. To overcome this, the `max_age` property allows to define a maximum
    age, after which older chunks will no longer be considered.

    Properties
    ----------
    interval : int
        The interval in which chunks should be recomputed.
    max_age : int
        The maximum age of considered chunks, thus the lower `max_age`, the faster the retrieval.
    """

    def __init__(self, n_dims: int, storage: StorageStrategy, n_chunks: int, max_age: int):
        super().__init__(n_dims, storage)
        self.max_age = max_age
        self.n_chunks = n_chunks

    def get_outdated_ids(self, current_chunk: int):
        available_chunks = self.storage.get_available_chunks()
        if len(available_chunks) == 0:
          return empty((0, self.n_dims))

        interval = len(available_chunks) // self.n_chunks

        # updates based on location in the storage dataframe happen at the same int index:
        # [x][][x][][x][] --> ||max_storage||=6 and interval=2
        # so we update every item that falls into either of these positions
        # the interval we chose is set so that there are at most n_chunks in there
        if interval > 0:
          outdated_chunks = available_chunks[available_chunks % interval == 0]
        else:
          outdated_chunks = available_chunks

        outdated_chunks = outdated_chunks[-self.n_chunks:]
        outdated_items = self.storage.get_items_for_chunks(outdated_chunks.tolist(), as_df=True)

        if len(outdated_items) == 0:
          return empty((0, self.n_dims))

        outdated_ids = outdated_items[ID].to_numpy()
        return outdated_ids
