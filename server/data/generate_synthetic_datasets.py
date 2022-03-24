import pandas as pd
import numpy as np
from sklearn.datasets import make_blobs, make_swiss_roll


def generate_dataset(label: str, path: str, args):
  dataset = None
  if "blobs" in label:
    dataset, _ = make_blobs(**args)
  elif label == "swiss_roll":
    dataset, _ = make_swiss_roll(**args)
  elif label == "sorted1M":
    dataset = generate_sorted_dataset(**args)

  if dataset is not None:
    # write to file
    df = pd.DataFrame(dataset)
    df.to_csv(path, index_label="tripID")  # HACK until use case config is made globally available.


def generate_sorted_dataset(n_samples: int):
  return pd.DataFrame(np.arange(n_samples))


n_samples = 1000000
path = "./"

default_parameters = {
  "1blobs": {
    "n_samples": n_samples,
    "n_features": 2,
    "centers": 1,
    "cluster_std": 2.0,
    "random_state": 0,
  },
  "4blobs": {
    "n_samples": n_samples,
    "n_features": 4,
    "centers": 4,
    "cluster_std": 0.75,
    "random_state": 0,
  },
  "10blobs": {
    "n_samples": n_samples,
    "n_features": 10,
    "centers": 10,
    "cluster_std": 1,
    "random_state": 0,
  },
  # "swiss_roll": {
  #   "n_samples": n_samples,
  #   "random_state": 0
  # },
  # "sorted1M": {
  #   "n_samples": 1000000
  # }
}


if __name__ == "__main__":
  for key in default_parameters:
    generate_dataset(key, f"{path}/{key}.csv", default_parameters[key])
