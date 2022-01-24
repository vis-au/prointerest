from numpy import empty
from sklearn.utils.random import sample_without_replacement

from database import ID
from storage_strategy.storage_strategy import StorageStrategy

from .context_item_selection_strategy import ContextItemSelectionStrategy


class MostRecentChunkBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_chunks: int) -> None:
        super().__init__(n_dims, storage)
        self.n_chunks = n_chunks  # how many most recent chunks should be returned as context?

    def get_context_ids(self, n: int, current_chunk: int):
        # get the n most recent chunks from the database that are available in storage
        stored_chunks = self.storage.get_available_chunks()
        most_recent_chunks = stored_chunks[-self.n_chunks:]

        most_recent_items = self.storage.get_items_for_chunks(
            most_recent_chunks.tolist(),
            as_df=True
        )

        if len(most_recent_items) == 0:
            return empty(0)

        most_recent_ids = most_recent_items[ID].iloc[:n].to_numpy()
        return most_recent_ids


class RandomChunkBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_chunks: int):
        super().__init__(n_dims, storage)
        self.n_chunks = n_chunks  # how many most recent chunks should be returned as context?

    def get_context_ids(self, n: int, current_chunk=None):
        # if the number of processed chunks is lower than the number of chunks that should be
        # returned as context, just return all chunks.
        all_chunks = self.storage.get_available_chunks()
        n_population = len(all_chunks)

        if n_population == 0:
            return empty((0, self.n_dims))

        if n_population < self.n_chunks:
            chunks = all_chunks
        else:
            sampled_indeces = sample_without_replacement(n_population, self.n_chunks)
            chunks = all_chunks[sampled_indeces]

        items_in_chunks = self.storage.get_items_for_chunks(chunks, as_df=True)
        context_ids = items_in_chunks[ID].iloc[:n].to_numpy()
        return context_ids
