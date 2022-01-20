import pandas as pd
import numpy as np
from sklearn.datasets import make_blobs, make_swiss_roll


def generate_dataset(label: str, path: str, args):
  dataset = None
  if label == "blobs":
    dataset, _ = make_blobs(**args)
  elif label == "swiss_roll":
    dataset, _ = make_swiss_roll(**args)

  if dataset is not None:
    # write to file
    df = pd.DataFrame(dataset)
    df.to_csv(path, index_label="tripID")  # HACK until use case config is made globally available.


def generate_sorted_dataset(size: int, path: str):
  df = pd.DataFrame(np.arange(size))
  df.to_csv(path, index_label="tripID")


n_samples = 1000000
path = "./"

default_parameters = {
  "blobs": {
    "n_samples": n_samples,
    "n_features": 2,
    "centers": 1,
    "cluster_std": 2.0,
    "random_state": 0,
  },
  "swiss_roll": {
    "n_samples": n_samples,
    "random_state": 0
  }
}


if __name__ == "__main__":
  for key in default_parameters:
    generate_dataset(key, f"{path}/{key}.csv", default_parameters[key])
  generate_sorted_dataset(1000000, f"{path}/sorted1M.csv")
