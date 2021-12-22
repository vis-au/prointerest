from random import randint
from database import ID, CHUNK, get_from_processed
from .context_item_selection_strategy import ContextItemSelectionStrategy


class MostRecentChunkBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, n_chunks: int) -> None:
        super().__init__(n_dims)
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
    def __init__(self, n_dims: int, n_chunks: int) -> None:
        super().__init__(n_dims)
        self.n_chunks = n_chunks  # how many most recent chunks should be returned as context?

    def get_context_ids(self, current_chunk: int):
        # if the number of processed chunks is lower than the number of chunks that should be
        # returned as context, just return all chunks.
        if current_chunk < self.n_chunks:
            random_chunk_ids = range(current_chunk)
        else:
            random_chunk_ids = [randint(0, current_chunk) for _ in range(self.n_chunks)]

        ids_list = [str(id) for id in random_chunk_ids]
        ids_sql = ",".join(ids_list)
        context_ids = get_from_processed([f"{CHUNK} IN ({ids_sql})"], ID, as_df=True)
        return context_ids[ID.lower()].to_numpy()