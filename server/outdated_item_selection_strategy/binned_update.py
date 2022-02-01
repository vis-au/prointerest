import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.random import sample_without_replacement
from .outdated_item_selection_strategy import OutdatedItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy
from database import ID


class BinnedUpdate(OutdatedItemSelectionStrategy):
    """
    Outdated item detection strategy that updates the data in bins.
    """

    def __init__(self, n_dims: int, storage: StorageStrategy, n_bins: int):
        super().__init__(n_dims, storage)
        self.n_bins = n_bins
        self.outdated_bin = 0

    def get_outdated_ids(self, n: int, current_chunk: int):
        outdated_ids_dois = self.storage.get_available_dois(with_ids=True)

        if len(outdated_ids_dois) == 0:
            return pd.DataFrame()

        binning = KBinsDiscretizer(n_bins=self.n_bins, strategy="uniform", encode="ordinal")
        bins: np.ndarray = binning.fit_transform(outdated_ids_dois[:, 1].reshape(-1, 1))

        bins = bins.reshape(-1, ).astype(np.int64)
        outdated_ids = outdated_ids_dois[:, 0][bins == self.outdated_bin]

        if len(outdated_ids) > n:
            outdated_indeces = sample_without_replacement(len(outdated_ids), n)
            outdated_ids = outdated_ids[outdated_indeces]
        elif len(outdated_ids) < n:
            remaining_ids = outdated_ids_dois[:, 0][bins != self.outdated_bin]

            n_population = len(remaining_ids)
            n_samples = n - len(outdated_ids)
            if n_population < n_samples:
                n_population = n_samples

            additional_ids = sample_without_replacement(n_population, n_samples)
            outdated_ids = np.append(outdated_ids, additional_ids)

        self.outdated_bin = (self.outdated_bin + 1) % self.n_bins
        return outdated_ids
