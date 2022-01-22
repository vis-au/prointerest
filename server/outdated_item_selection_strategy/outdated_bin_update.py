from numpy import empty
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy


class OutdatedBinUpdate(OutdatedItemSelectionStrategy):
    """
    Outdated item detection strategy that compares binnings before and after the computation of
    the doi value to determine items that are outdated, as their bin has changed significantly.
    """

    def get_outdated_bins(self):
        return ()  # TODO: given bins before and after an update, find those that need updating.

    def get_outdated_ids(self, current_chunk: int):
        outdated = self.get_outdated_bins()
        if len(outdated) == 0:
            return empty((0,))
        if len(outdated) == 1:
            outdated += outdated  # make sure tuple() below works

        return empty((0,))
