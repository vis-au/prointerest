from numpy import empty
from sklearn.utils.random import sample_without_replacement

from database import ID, CHUNK, get_from_processed
from storage_strategy.storage_strategy import StorageStrategy

from .context_item_selection_strategy import ContextItemSelectionStrategy


class MostRecentChunkBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_chunks: int) -> None:
        super().__init__(n_dims, storage)
        self.n_chunks = n_chunks  # how many most recent chunks should be returned as context?

    def get_context_ids(self, current_chunk: int):
        # if the number of processed chunks is lower than the number of chunks that should be
        # returned as context, just return all chunks.
        if current_chunk < self.n_chunks:
            latest_chunk = 0
        else:
            # return the last n_chunks chunks
            latest_chunk = current_chunk - self.n_chunks

        # assuming that storage is greater or equal in size as n_chunks * chunk_size
        context_ids = get_from_processed([f"{CHUNK} > {latest_chunk}"], ID, as_df=True)
        return context_ids[ID.lower()].to_numpy()


class RandomChunkBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_chunks: int):
        super().__init__(n_dims, storage)
        self.n_chunks = n_chunks  # how many most recent chunks should be returned as context?

    def get_context_ids(self, current_chunk=None):
        # if the number of processed chunks is lower than the number of chunks that should be
        # returned as context, just return all chunks.
        all_chunks = self.storage.get_available_chunks()
        n_population = len(all_chunks)

        if n_population == 0:
            return empty((0, self.n_dims))
        if current_chunk < self.n_chunks:
            chunks = all_chunks
        else:
            sampled_indeces = sample_without_replacement(n_population, self.n_chunks)
            chunks = all_chunks[sampled_indeces]

        items_in_chunks = self.storage.get_items_for_chunks(chunks, as_df=True)
        context_ids = items_in_chunks[ID].to_numpy()
        return context_ids
