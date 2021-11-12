from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from database import ID, CHUNK, get_from_processed

class RegularIntervalUpdate(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that retrieves items in regular intervals, such that an item
  becomes outdated every `interval` steps.

  This strategy is presumably the most costly, as the number of outdated chunks grows linearly with
  each processed chunk. To overcome this, the `max_age` property allows to define a maximum age,
  after which older chunks will no longer be considered.

  Properties
  ----------
  interval : int
    The interval in which chunks should be recomputed.
  max_age : int
    The maximum age of considered chunks, thus the lower `max_age`, the faster the retrieval.
  '''
  def __init__(self, n_dims: int, interval: int, max_age : int):
    super().__init__(n_dims)
    self.interval = interval
    self.max_age = max_age

  def get_outdated_ids(self, current_chunk: int):
    res = get_from_processed([
      f"MOD({CHUNK}, {current_chunk})=0",
      f"CHUNK < {self.max_age}"
    ], as_df=True)

    return res[ID.lower()].to_numpy()