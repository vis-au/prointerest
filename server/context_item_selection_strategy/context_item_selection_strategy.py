from numpy import empty, ndarray
from database import get_items_for_ids

class ContextItemSelectionStrategy:
  def __init__(self, n_dims: int) -> None:
    self.n_dims = n_dims

  def get_context_ids(self, current_chunk: int) -> ndarray:
    return empty(0)

  def get_context_items(self, current_chunk: int) -> ndarray:
    ''' Takes the `ids` of items comptued in `get_context_ids` and retrieves the actual data from
    the database. Returns an ndarray of shape (n, m).

    Parameters
    ----------
    current_chunk : int
      The index of the current chunk.
    '''
    context_ids = self.get_context_ids(current_chunk)
    if len(context_ids) == 0:
      return empty(0)

    context_id_list = context_ids.tolist()
    return get_items_for_ids(context_id_list)