from xml.dom import NOT_SUPPORTED_ERR
import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.utils.random import sample_without_replacement
from storage_strategy.storage_strategy import ID, StorageStrategy
from .context_item_selection_strategy import ContextItemSelectionStrategy


# the idea for doi based context strategy is we use the computed doi values to find good candidates
# to include as context. To this end, we divide the data in storage into bins from which we then
# sample the context. There are many suitable distributions we may use, based on dataset and the
# task at hand:
#  * normal distribution: most context items in the 0.4-0.6 range
#  * min/max: oversample high and low doi values, undersample the intermediate values
#  * even cardinality: the same number of items get sampled per bin
#  * uniform: items are sampled randomly acros bins, such that the doi distribution in the
#    context is the same as in storage

class DoiBasedContext(ContextItemSelectionStrategy):
  def __init__(self, n_dims: int, storage: StorageStrategy, n_bins: int, n_samples: int,
               strategy: str = "min_max") -> None:
    super().__init__(n_dims, storage)
    self.n_bins = n_bins
    self.n_samples = n_samples
    self.strategy = strategy

  def _get_doi_bins_from_storage(self) -> pd.DataFrame:
    id_dois = self.storage.get_available_dois(with_ids=True)

    if len(id_dois) == 0:
      return pd.DataFrame()

    binning = KBinsDiscretizer(n_bins=self.n_bins, strategy="uniform", encode="ordinal")
    bin_per_id = binning.fit_transform(id_dois[:, 1].reshape(-1, 1))

    id_dois_df = pd.DataFrame(id_dois, columns=[ID, "doi"])
    id_dois_df["bin"] = bin_per_id
    return id_dois_df

  def _get_samples_per_bin(self):
    # from every bin, we draw the same number of ids
    if self.strategy == "uniform":
      samples_per_bin = np.ones((self.n_bins, )) * (self.n_samples // self.n_bins)
    # otherwise, use a normal distribution to decide on the sample frequency per bin
    elif self.strategy == "normal" or self.strategy == "min_max":
      rng = np.random.default_rng()
      draw = rng.normal(size=self.n_samples)
      samples_per_bin = np.histogram(draw, bins=self.n_bins)[0]
    else:
      raise Exception("unknown sampling strategy in doi based context")

    if self.strategy == "min_max":
      # the mean of the normal distribution above now sits at the min and max bins
      samples_per_bin = np.roll(samples_per_bin, len(samples_per_bin) // 2)

    return samples_per_bin

  def get_context_ids(self, current_chunk: int) -> np.ndarray:
    bin_per_id_df = self._get_doi_bins_from_storage()

    if len(bin_per_id_df) == 0:
      return np.empty((0, self.n_dims))

    outdated_ids = np.array([])
    samples_per_bin = self._get_samples_per_bin()
    # from every bin, get a number of ids from the stored data, according to samples_per_bin
    for i in range(self.n_bins):
      ids_in_bin = bin_per_id_df[bin_per_id_df["bin"] == i]
      n_population = len(ids_in_bin)
      n_samples = min(samples_per_bin[i], n_population)
      picks = sample_without_replacement(n_population=n_population, n_samples=n_samples)
      outdated_ids_bin = ids_in_bin.iloc[picks][ID].to_numpy()
      outdated_ids = np.append(outdated_ids, outdated_ids_bin)

    # some bins may be smaller than the number of samples we want to draw from them, so there can be
    # "open spots" that we can fill randomly
    n_open_spots = self.n_samples - len(outdated_ids)
    if n_open_spots > 0:
      remaining_ids = bin_per_id_df[~bin_per_id_df[ID].isin(outdated_ids)][ID]
      if len(remaining_ids) > 0:
        n_samples = min(n_open_spots, len(remaining_ids))
        filler_picks = sample_without_replacement(len(remaining_ids), n_samples)
        filler_ids = remaining_ids.iloc[filler_picks]
        outdated_ids = np.append(outdated_ids, filler_ids)

    return outdated_ids
