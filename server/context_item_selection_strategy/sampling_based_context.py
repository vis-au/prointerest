from pandas import DataFrame
from sklearn.utils.random import sample_without_replacement
from database import ID, get_from_data
from .context_item_selection_strategy import ContextItemSelectionStrategy


class RandomSamplingBasedContext(ContextItemSelectionStrategy):
    def __init__(self, n_dims: int, n_samples: int) -> None:
        self.n_samples = n_samples

    def get_context_items(self, current_chunk: int):
        data = get_from_data(["TRUE"], as_df=True)
        sample = sample_without_replacement(
            len(data[ID]), self.n_samples, random_state=0
        )
        df = DataFrame(data)
        return df.loc[sample]


class ReservoirSamplingBasedContext(ContextItemSelectionStrategy):
    pass