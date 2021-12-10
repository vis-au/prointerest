from typing import final
import numpy as np
from database import get_items_for_ids


class OutdatedItemSelectionStrategy:
    def __init__(self, n_dims: int):
        self.n_dims = n_dims

    def get_outdated_ids(self, current_chunk: int) -> np.ndarray:
        """This function is to be overwritten by the particular subclass strategy. It computes the
        `ids` of items that are outdated, based on some heuristic.

        Returns an ndarray of shape (n, )."""
        return np.empty((0,))

    @final
    def get_outdated_items(self, current_chunk: int) -> np.ndarray:
        """Takes the `ids` of items computed in `get_outdated_ids` and retrieves the actual data from
        the database. Returns an ndarray of shape (n, m).

        Parameters
        ----------
        current_chunk : int
          The index of the current chunk.
        """
        outdated_ids = self.get_outdated_ids(current_chunk)
        if len(outdated_ids) == 0:
            return np.empty((0, self.n_dims))
        outdated_id_list = outdated_ids.tolist()
        return get_items_for_ids(outdated_id_list)
