from numpy import empty
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy

class NoUpdate(OutdatedItemSelectionStrategy):
  '''' Outdated item detection strategy that never detects any outdated items.'''
  def get_outdated_ids(self, current_chunk: int):
    return empty((0, self.n_dims))