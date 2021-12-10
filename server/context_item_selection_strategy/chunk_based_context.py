from database import ID, CHUNK, get_from_processed
from .context_item_selection_strategy import ContextItemSelectionStrategy


class ChunkBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, n_chunks) -> None:
        super().__init__(n_dims)
        self.n_chunks = n_chunks

    def get_context_ids(self, current_chunk: int):
        if self.n_chunks > current_chunk:
            latest_chunk = 0
        else:
            latest_chunk = current_chunk - self.n_chunks

        context_ids = get_from_processed([f"{CHUNK} > {latest_chunk}"], ID, as_df=True)
        return context_ids[ID.lower()].to_numpy()
