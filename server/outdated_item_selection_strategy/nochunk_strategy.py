from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from database import ID, get_from_processed

class NoChunkStrategy(OutdatedItemSelectionStrategy):
  '''' Outdated item detection strategy that never detects any outdated items.'''
  def get_outdated_ids(self, current_chunk: int):
    res = get_from_processed(["FALSE"], as_numpy=True)

    return res[ID.lower()]