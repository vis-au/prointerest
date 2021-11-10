import numpy as np
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from database import ID, CHUNK, get_from_processed

class OutdatedBinStrategy(OutdatedItemSelectionStrategy):
  ''' Outdated item detection strategy that compares binnings before and after the computation of
  the doi value to determine items that are outdated, as their bin has changed significantly.
  '''
  def get_outdated_bins(self):
    return () # TODO: given bins before and after an update, find those that need updating.

  def get_outdated_ids(self, current_chunk: int):
    outdated = self.get_outdated_bins()
    if len(outdated) == 0:
      return np.empty((0,))
    res = get_from_processed([
      f"{CHUNK} IN {str(tuple(outdated))}"
    ], as_numpy=True)

    return res[ID.lower()]