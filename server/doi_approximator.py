import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KDTree
from storage_strategy.progressive_bin_sampler import ProgressiveBinSampler
from typing import final


class DoiApproximator:
  ''' Helper class for either computing or approximating the doi function over the next chunk of
  data, taking into account previously seen data.

  Properties
  ----------
  doi : np.ndarray -> np.ndarray
    the degree of interest function.
  chunk_size : int
    the items processed per chunk (currently only supports static chunks).
  n_dims : int
    the number of dimensions in the data (currently only supports fixed-size data).
  '''
  def __init__(self, doi, n_dims) -> None:
    self.doi = doi
    self.sampler = ProgressiveBinSampler(n_dims=n_dims)
    self.processed = 0

  def compute_doi(self, i, chunk, X_sample, y_sample) -> np.ndarray:
    ''' Computes the degree-of-interest function for the given chunk under the context of the data
      sampled from previous increments.

    Parameters
    ----------
    i : int
      Index of the current chunk.
    chunk : np.ndarray
      The next chunk of the data. Has shape (n, m).
    X_sample : np.ndarray
      The contextual data from previous chunks, provided by `self.sampler`. Has shape(n, m).
    y_sample : np.ndarray
      The doi values for the items in `X_sample`. Has shape (n, )
    '''
    pass

  @final
  def get_next(self, i: int, chunk: np.ndarray):
    ''' Computes the next increment of doi values over a given set of new items.

    Takes into account also previously seen data and updates "outdated" values. What values are
    considered outdated is controlled by the particular UpdateSelectionStrategy used in the
    subclass.

    Parameters:
    -----------
    i : int
      Index of the current chunk.
    chunk : np.ndarray
      The next chunk of the data. Has shape (n, m).
    '''
    if i == 0:
      X_sample = np.empty((0, chunk.shape[1]))
      y_sample = np.empty((0, ))
    else:
      X_sample, y_sample = self.sampler.get_current_sample(return_labels=False)

    y = self.compute_doi(i, chunk, X_sample, y_sample)

    _, _, labels, edges = self.sampler.add_chunk(chunk, y, self.processed, compute_edges=True)
    self.processed += len(chunk)

    return y, labels, edges


class ActualDoiEvaluator(DoiApproximator):
  def compute_doi(self, i, chunk, X_sample, y_sample) -> np.ndarray:
    X_ = np.append(X_sample, chunk, axis=0)
    y_ = self.doi(X_)

    new_doi_values = y_[len(X_sample):]
    return new_doi_values


class RegressionTreeApproximator(DoiApproximator):
  def __init__(self, doi, chunk_size, n_dims) -> None:
    super().__init__(doi, chunk_size, n_dims)
    self.tree = DecisionTreeRegressor()

  def compute_doi(self, i, chunk, X_sample, y_sample):
    if i == 0:
      new_doi_values = np.empty((len(X_sample), ))
    else:
      self.tree.fit(X_sample, y_sample)
      new_doi_values = self.tree.predict(chunk)

    return new_doi_values


class KDTreeBasedApproximator(DoiApproximator):
  def __init__(self, doi, chunk_size, n_dims) -> None:
    super().__init__(doi, chunk_size, n_dims)

  def compute_doi(self, i, chunk, X_sample, y_sample):
    kdtree = KDTree(X_sample)

    knns = kdtree.query(chunk).reshape(-1, )
    new_doi_values = y_sample[knns]

    return new_doi_values