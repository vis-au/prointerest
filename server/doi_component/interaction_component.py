import pandas as pd
import numpy as np
from typing import List

from .doi_component import DoiComponent


class InteractionComponent(DoiComponent):
    window_size: int  # how many interactions to consider for the doi?
    interaction_log: List[
        List[str]
    ]  # stores the ids of items affected by interaction at t_i
    interaction_counts: dict

    def __init__(self, window_size: int = 10) -> None:
        super().__init__()
        self.window_size = window_size
        self.clear()

    def clear(self):
        """Reset the component."""

        self.interaction_log = []
        self.interaction_counts = {}

    def log_interaction(self, affected_item_ids: List[str]):
        """Saves the interaction and updates the counts for the ids in the provided list."""

        self.interaction_log += [affected_item_ids]

        for item_id in affected_item_ids:
            if item_id in self.interaction_counts:
                self.interaction_counts[item_id] += 1
            else:
                self.interaction_counts[item_id] = 1

    def _undo_interaction(self, interaction: List[str]):
        """Reduces the counter for each id in the interaction and deleted them if 0."""

        for id in interaction:
            if str(id) in self.interaction_counts:
                self.interaction_counts[str(id)] -= 1

                if self.interaction_counts[str(id)] == 0:
                    del self.interaction_counts[str(id)]

    def _undo_interactions(self, interactions: List[List[str]]):
        """Undos the interactions provided by reducing the counter for each affected item."""

        for interaction in interactions:
            self._undo_interaction(interaction)

    def undo_outdated_interactions(self):
        """
        Make sure that only the last <window_size> interactions are in self.id_log, undo the rest.
        """

        outdated_interactions = self.interaction_log[: -self.window_size]
        self._undo_interactions(outdated_interactions)

    def get_interaction_count_matrix(self):
        """Converts the interaction_counts dict to a DataFrame."""

        np_lists = np.array(
            [
                list(self.interaction_counts.keys()),
                list(self.interaction_counts.values()),
            ]
        )
        np_lists = np_lists.astype(int)  # id column must be of type int to match X

        np_matrix = np_lists.T  # np_lists has shape 2xn, so transpose it to nx2
        M = pd.DataFrame(np_matrix, columns=["id", "count"])
        M.set_index("id", inplace=True)  # make id the index column
        return M

    def compute_doi(self, X: pd.DataFrame):
        """
        Finds out how often each item in X has been interacted with within the last <window_size>
        interactions, and then scales that number by <window_size>.
        """
        M = self.get_interaction_count_matrix()  # get interaction counts as matrix

        X.set_index(0, inplace=True)

        Y = X.join(M, how="left")  # for all rows not in M the "count" column is NaN
        Y.loc[Y["count"].isna(), "count"] = 0  # set NaN to 0

        Y_doi = Y["count"] / self.window_size
        return Y_doi
