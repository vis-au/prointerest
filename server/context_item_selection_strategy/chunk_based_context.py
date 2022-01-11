from random import randint
from numpy import empty
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

        context_ids = get_from_processed([f"{CHUNK} > {latest_chunk}"], ID, as_df=True)
        return context_ids[ID.lower()].to_numpy()


class RandomChunkBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, storage: StorageStrategy, n_chunks: int) -> None:
        super().__init__(n_dims, storage)
        self.n_chunks = n_chunks  # how many most recent chunks should be returned as context?

    def get_context_ids(self, current_chunk: int):
        # if the number of processed chunks is lower than the number of chunks that should be
        # returned as context, just return all chunks.
        if current_chunk < self.n_chunks:
            random_chunk_ids = range(current_chunk)
        else:
            random_chunk_ids = [randint(0, current_chunk) for _ in range(self.n_chunks)]
        if len(random_chunk_ids) == 0:
            return empty((0, self.n_dims))

        ids_list = [str(id) for id in random_chunk_ids]
        if len(ids_list) == 1:
            ids_list += ids_list  # make sure tuple() below works
        context_ids = get_from_processed([f"{CHUNK} IN {tuple(ids_list)}"], ID, as_df=True)
        return context_ids[ID.lower()].to_numpy()
