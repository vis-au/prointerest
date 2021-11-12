from random import randint
import numpy as np
from sklearn.utils.random import sample_without_replacement


class ProgressiveBinSampler():
  def __init__(self, reservoir_size=1000, n_bins=5, n_dims=2) -> None:
    self.reservoir_size = reservoir_size
    self.n_bins = n_bins
    self.n_dims = n_dims
    self.X_reservoir: dict[str, np.ndarray] = {}
    self.y_reservoir: dict[str, np.ndarray] = {}
    self.skips = [self.reservoir_size for _ in range(self.n_bins)]
    self.reset_reservoirs()


  def reset_reservoirs(self):
    '''Reset all reservoirs.

    Returns
    -------
    self.X_reservoir : dict[str, np.ndarray]
      A dictionary of empty bins, indexed by bin labels from `bin`.
    self.y_reservoir : dict[str, np.ndarray]
      A dictionary of empty bins, indexed by bin labels from `bin`.
    '''

    # flush the reservoirs
    self.X_reservoir = {}
    for i in range(self.n_bins):
      self.X_reservoir[i] = np.empty((0, self.n_dims))
      self.y_reservoir[i] = np.empty((0, ))

    # reset the skip counter
    self.skips = [self.reservoir_size for _ in range(self.n_bins)]

    return self.X_reservoir, self.y_reservoir


  def get_current_sample(self, return_labels=False):
    '''Helper function that returns all items across all reservoirs as ndarrays.

    Parameters
    ----------
    return_labels : boolean (default: False)
      Controls whether this function also returns the labels for the data, i.e., the y values that
      were passed to `add_chunk()`.

    Returns
    -------
    X_sample : np.ndarray
      Array-like containing all items currently in the reservoir. Has shape (p, m), where `p` is
      at least 0 and at most `n_bins * reservoir_size` big.
    y_sample : np.ndarray
      Only returned if `return_labels` is set to `True`.
      Array-like containing all labels currently in the reservoir. Has shape (p, ), where `p` is
      at least 0 and at most `n_bins * reservoir_size` big.
    '''

    X_sample = np.concatenate(tuple([self.X_reservoir[x] for x in self.X_reservoir]))

    if not return_labels:
      return X_sample

    y_sample = np.concatenate(tuple([self.y_reservoir[x] for x in self.y_reservoir]))
    return X_sample, y_sample


  def get_bin_edges(self, y: np.ndarray, bins: np.ndarray):
    '''Given the bins assigned to a set of numerical values, returns boundaries of these bins.

    The output is a list of boundary values x_0 to x_l for bins b_0 to b_l, such that
    x_j = min(b_j) and x_l = max(b_l).

    Parameters
    ----------
    y : np.ndarray
      DoI values, i.e., "list" of floating point values. Has shape (n, ).
    bins : np.ndarray
      Bin labels assigned to the DoI values in `y`. Has shape (n, ).

    Returns
    -------
    list[float]
      Bin boundaries from y.min() to y.max().
    '''
    edges = []
    max_label = np.max(bins)
    # add lower bounds per bin
    for i in range(max_label):
      edges += [np.min(y[bins == i])]

    # add upper bound
    edges += [np.max(y[bins == max_label])]
    return edges


  def _bin(self, y: np.ndarray):
    '''Sorts the input by value and then divides it into bin_size bins of equal size.

    If len(y) / n_bins has a residual, items assigned to the "overflow" bin are merged into the last
    one to guarantee n_bins.

    Parameters
    ----------
    y : np.ndarray
      DoI values, i.e., "list" of floating point values. Has shape (n, ).

    Returns
    -------
    index : np.ndarray
      An index that assigns the bin number to each item in `y`. Has shape (n, ).
    '''
    sort = np.argsort(y.flatten())
    total_size = len(y)
    bin_size = total_size // self.n_bins
    index = np.arange(0, total_size)
    index[sort] = index // bin_size

    # merge "residual" bin with last bin to guarantee n_bins in output
    if total_size // self.n_bins != total_size / self.n_bins:
      index[index == self.n_bins] = self.n_bins - 1

    return index


  def _reservoir_sample_by_bin(self, X: np.ndarray, y: np.ndarray, bins: np.ndarray, processed: int):
    ''' Takes the next chunk of data and samples it into bins based on the y value returned by a
    doi function.

    By using a reservoir sampling strategy, this function ensures that the range of doi values is
    evenly represented in the sample, even between progressive updates. This is necessary, since
    doi functions often produce a skewed result space, where only few items are assigned a high
    value. To achieve even class distributions, this function basically undersamples
    high-cardinality classes.

    Parameters
    ----------
    X : np.ndarray
      The next chunk of data to be sampled into the reservoirs. Has shape (n, m).
    y : np.ndarray
      The labels for the next chunk of data to be sampled into the reservoirs. Has shape (n, ).
    bins : np.ndarray
      The bins assigned to each row in X (e.g. by `_bin()`). Has shape (n, ).
    processed : int
      The number of items processed so far. Used to get the per-item probability of being picked.

    Returns
    -------
    self.X_reservoir : dict[str, np.ndarray]
      A dictionary of data bins after sampling, indexed by bin labels from `bin`.
    self.y_reservoir : dict[str, np.ndarray]
      A dictionary of label bins after sampling, indexed by bin labels from `bin`.
    '''
    for j in range(self.n_bins):
      if len(bins[bins == j]) == 0:
        continue

      # get all items currently in this bin
      X_in_bin = X[(bins == j).flatten()]
      y_in_bin = y[(bins == j).flatten()]

      # find all items currently in the reservoir for this bin
      bin_reservoir_X = self.X_reservoir[j]
      bin_reservoir_y = self.y_reservoir[j]
      skip = self.skips[j]

      in_bin = len(X_in_bin)
      in_reservoir = len(bin_reservoir_X)

      # reservoir sample the bin using items assigned to this bin in the current iteration
      # before replacing, fill the reservoir
      if in_reservoir < self.reservoir_size:
        # either pick all, if there is space, or just pick enough to fill
        if in_reservoir == 0 and in_bin < self.reservoir_size:
          sample = np.arange(in_bin) # pick all elements in the chunk
        else:
          n_samples = np.min((self.reservoir_size-in_reservoir, in_bin))
          sample = sample_without_replacement(n_population=in_bin, n_samples=n_samples, random_state=randint(0, j))

        bin_reservoir_X = np.concatenate((bin_reservoir_X, X_in_bin[sample]))
        bin_reservoir_y = np.concatenate((bin_reservoir_y, y_in_bin[sample]))
        skip = randint(0, processed+len(X))

      # replace items in the bin with a probability of 1/N per item throughout the progression
      else:
        while skip < processed:
          candidate_X = X_in_bin[skip % in_bin]
          candidate_y = y_in_bin[skip % in_bin]
          pick = randint(0, self.reservoir_size-1)
          bin_reservoir_X[pick] = candidate_X
          bin_reservoir_y[pick] = candidate_y
          skip = randint(0, processed+len(X))

      self.skips[j] = skip
      self.X_reservoir[j] = bin_reservoir_X
      self.y_reservoir[j] = bin_reservoir_y

    return self.X_reservoir, self.y_reservoir


  def add_chunk(self, X: np.ndarray, y: np.ndarray, processed: int, compute_edges=False):
    ''' Adds a new chunk to the sample using reservoir sampling.

    Parameters
    ----------
    X : np.ndarray
      The new chunk. Has shape (n, m).
    y : np.ndarray
      Numeric values assigned to each item in the chunk. Has shape (n, ).
    processed : int
      The number of items processed in the computation so far.
    compute_edges : boolean
      Whether or not the bin edges should be returned as well.

    Returns
    -------
    X_res : dict[str, np.ndarray]
      A dictionary of data bins after sampling, indexed by bin labels from `bin`.
    y_res : dict[str, np.ndarray]
      A dictionary of label bins after sampling, indexed by bin labels from `bin`.
    labels : np.ndarray
      The bins computed for each item in y. Has shape (n, ).
    edges : list[number]
      The bin edges for the computed bins
    '''
    # labels can be used to index both X and y
    labels = self._bin(y)
    self._reservoir_sample_by_bin(X, y, labels, processed)

    if compute_edges:
      edges = self.get_bin_edges(y, labels)
      return self.X_reservoir, self.y_reservoir, labels, edges
    else:
      return self.X_reservoir, self.y_reservoir, labels
