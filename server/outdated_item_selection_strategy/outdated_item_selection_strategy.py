from typing import final
import numpy as np
import pandas as pd

from database import ID
from storage_strategy.storage_strategy import StorageStrategy


class OutdatedItemSelectionStrategy:
    def __init__(self, n_dims: int, storage: StorageStrategy):
        self.n_dims = n_dims
        self.storage = storage

    def get_outdated_ids(self, n: int, current_chunk: int) -> np.ndarray:
        """This function is to be overwritten by the particular subclass strategy. It computes the
        `ids` of items that are outdated, based on some heuristic.

        Returns an ndarray of shape (n, )."""
        return np.empty((0,))

    @final
    def get_outdated_items(self, n: int, current_chunk: int) -> pd.DataFrame:
        """Takes the `ids` of items computed in `get_outdated_ids` and retrieves the actual data
        from the database. Returns an ndarray of shape (n, m).

        Parameters
        ----------
        n : int
            The number of context items to be retrieved.
        current_chunk : int
            The index of the current chunk.
        """
        outdated_ids = self.get_outdated_ids(n, current_chunk)
        if len(outdated_ids) == 0:
            # dataframe of items, even if empty, is expected to have the id column
            empty = pd.DataFrame(np.empty((0, self.n_dims)))
            empty = empty.rename(columns={0: ID})
            return empty

        outdated_id_list = outdated_ids.tolist()
        return self.storage.get_items_for_ids(outdated_id_list, as_df=True)
