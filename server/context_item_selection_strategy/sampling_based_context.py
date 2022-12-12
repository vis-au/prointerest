from sklearn.utils.random import sample_without_replacement
from .context_item_selection_strategy import ContextItemSelectionStrategy
from storage_strategy.storage_strategy import StorageStrategy


class RandomSamplingBasedContext(ContextItemSelectionStrategy):
    def get_context_ids(self, n: int, current_chunk: int):
        stored_ids = self.storage.get_available_ids().to_numpy()

        processed = len(stored_ids)
        sample_size = processed if processed < n else n
        sample = sample_without_replacement(
            processed, sample_size, random_state=current_chunk
        )
        sampled_ids = stored_ids[sample]
        return sampled_ids


class ReservoirSamplingBasedContext(ContextItemSelectionStrategy):
    pass
