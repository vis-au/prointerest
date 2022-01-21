from os import listdir
from numpy import empty
from sklearn.utils.random import sample_without_replacement
from .context_item_selection_strategy import ContextItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy
from database import ID, get_from_processed


class RandomSamplingBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_samples: int) -> None:
        super().__init__(n_dims, storage)
        self.n_samples = n_samples

    def get_context_ids(self, current_chunk: int):
        stored_ids = self.storage.get_available_ids().to_numpy()

        processed = len(stored_ids)
        sample_size = processed if processed < self.n_samples else self.n_samples
        sample = sample_without_replacement(
            processed,
            sample_size,
            random_state=0
        )
        sampled_ids = stored_ids[sample]
        return sampled_ids


class ReservoirSamplingBasedContext(ContextItemSelectionStrategy):
    pass
