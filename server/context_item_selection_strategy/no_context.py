from numpy import empty
from .context_item_selection_strategy import ContextItemSelectionStrategy


class NoContext(ContextItemSelectionStrategy):
    def get_context_ids(self, current_chunk: int):
        return empty((0, self.n_dims))
