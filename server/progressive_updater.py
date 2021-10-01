import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KDTree
from typing import Tuple, final

from server.progressive_bin_sampler import ProgressiveBinSampler

class ProgressiveUpdater:
  def __init__(self, doi, chunk_size, n_dims) -> None:
    self.doi = doi
    self.chunk_size = chunk_size
    self.doi_values: np.ndarray = None
    self.sampler = ProgressiveBinSampler(n_dims=n_dims)
    self.doi_value_chunk = np.array((0, )) # stores the chunk at which the data was seen first
    self.updated_doi_values = np.array((0, )) # stores the doi values after the update
    self.processed = 0

  def update(self, i, chunk, X_sample, y_sample) -> Tuple[np.ndarray, np.ndarray]:
    pass

  @final
  def get_next(self, i: int, X: np.ndarray):
    if i == 0:
      X_sample = np.empty((0, X.shape[1]))
      y_sample = np.empty((0, ))
    else:
      X_sample, y_sample = self.sampler.get_current_sample(return_labels=True)

    y, updated_doi_values = self.update(i, X, X_sample, y_sample)
    self.doi_values = updated_doi_values

    _, _, labels, edges = self.sampler.add_chunk(X, y, self.processed)
    self.processed += len(X)

    # save the iteration at which an item was retrieved
    age = np.full_like(y, fill_value=i)
    self.doi_value_chunk = np.append(self.doi_value_chunk, age)

    return y, labels, edges


class RegressionTreeProgressiveUpdater(ProgressiveUpdater):
  def __init__(self, doi, chunk_size, n_dims) -> None:
      super().__init__(doi, chunk_size, n_dims)
      self.tree = DecisionTreeRegressor()


  def update(self, i, chunk, X_sample, y_sample):
    y_ = self.doi(chunk)

    if i > 0:
      self.tree.fit(X_sample, y_sample)
      y2 = self.tree.predict(chunk)
      y_ = np.mean([y_, y2], axis=0)

    new_doi_values = y_
    updated_doi_values = np.append(self.doi_values, new_doi_values)

    return new_doi_values, updated_doi_values


class RegularIntervalProgressiveUpdater(ProgressiveUpdater):
  def __init__(self, doi, chunk_size, n_dims, X: np.ndarray, max_age=10) -> None:
      super().__init__(doi, chunk_size, n_dims)
      self.X = X
      self.max_age = max_age


  def update(self, i, chunk, X_sample, y_sample):
    sample_size = len(X_sample)
    X_ = np.append(X_sample, chunk, axis=0)

    # add all chunks that haven't been updated in the last max_age iterations:
    added_index = {}
    for j in range(i):
      if j % self.max_age == 0:
        added_index[j] = len(X_) # store the beginning index for this chunk to find it later
        X_ = np.append(X_, self.X[j*self.chunk_size:(j+1)*self.chunk_size], axis=0)

    y_ = self.doi(X_)

    new_doi_values = y_[sample_size:sample_size + self.chunk_size]
    updated_doi_values = np.append(self.doi_values, new_doi_values)

    age = np.full_like(new_doi_values, fill_value=i)
    my_doi_value_chunk = np.append(self.doi_value_chunk, age)

    for j in range(1, i):
      if j % self.max_age == 0:
        index = added_index[j]
        updated_doi_values[my_doi_value_chunk == j] = y_[index:index+self.chunk_size]

    return new_doi_values, updated_doi_values


class KDTreeBasedProgressiveUpdater(ProgressiveUpdater):
  def __init__(self, doi, chunk_size, n_dims, X: np.ndarray) -> None:
      super().__init__(doi, chunk_size, n_dims)
      self.X = X

  def update(self, i, chunk, X_sample, y_sample):
      X_ = np.append(X_sample, chunk, axis=0)
      y_ = self.doi(X_)

      new_doi_values = y_[-self.chunk_size:]
      updated_doi_values = np.append(self.doi_values, new_doi_values)

      kdtree = KDTree(X_)

      if i > 0:
        # find knn in chunk for all points not in chunk
        knn = kdtree.query(self.X[:i*self.chunk_size], return_distance=False).reshape(-1, )
        updated_doi_values[:i*self.chunk_size] = y_[knn] # return type of query is odd

      return new_doi_values, updated_doi_values