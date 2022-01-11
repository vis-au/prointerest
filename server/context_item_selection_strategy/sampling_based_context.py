from sklearn.utils.random import sample_without_replacement
from .context_item_selection_strategy import ContextItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy
from database import ID, get_from_processed


class RandomSamplingBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_samples: int) -> None:
        super().__init__(n_dims, storage)
        self.n_samples = n_samples

    def get_context_ids(self, current_chunk: int):
        processed_ids = get_from_processed(["TRUE"], ID, as_df=True)[ID.lower()]

        sample = sample_without_replacement(len(processed_ids), self.n_samples, random_state=0)
        sampled_ids = processed_ids[sample]
        return sampled_ids


class ReservoirSamplingBasedContext(ContextItemSelectionStrategy):
    pass
