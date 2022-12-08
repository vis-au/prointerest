from numpy import empty, ndarray
from pandas import DataFrame

from storage_strategy.storage_strategy import StorageStrategy


class ContextItemSelectionStrategy:
    def __init__(self, n_dims: int, storage: StorageStrategy) -> None:
        self.n_dims = n_dims
        self.storage = storage

    def get_context_ids(self, n: int, current_chunk: int) -> ndarray:
        return empty(0)

    def get_context_items(self, n: int, current_chunk: int) -> ndarray:
        """Takes the `ids` of items computed in `get_context_ids` and retrieves the actual data from
        the database. Returns an ndarray of shape (n, m).

        Parameters
        ----------
        n : int
          The number of context items to be retrieved.
        current_chunk : int
          The index of the current chunk.
        """
        context_ids = self.get_context_ids(n, current_chunk)
        if len(context_ids) == 0:
            return DataFrame(empty((0, self.n_dims)))

        context_id_list = context_ids.tolist()
        return self.storage.get_items_for_ids(context_id_list, as_df=True)
