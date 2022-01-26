import pandas as pd
import numpy as np


# helper function that bins the doi column
def get_doi_bins_df(doi_df: pd.DataFrame, n_bins: int, with_labels=False) -> pd.DataFrame:
  histogram, edges = np.histogram(doi_df["doi"], bins=n_bins, range=(0, 1))
  bins_df = pd.DataFrame(histogram.transpose())

  if with_labels:
    labels = np.digitize(doi_df["doi"], bins=edges)
    return bins_df, labels
  else:
    return bins_df


# compute the difference bins
def get_doi_delta_bins_df(doi_bins_a: pd.DataFrame, doi_bins_b: pd.DataFrame, total_size: int,
                          n_bins: int):
  # copy the first df
  delta_bins = pd.DataFrame(doi_bins_a)
  delta_bins["delta"] = (doi_bins_a[0] - doi_bins_b[0]) / total_size
  delta_bins.columns = ["doi", "delta"]
  # delta_bins["delta"] = bins_a[0]

  # add context info
  delta_bins["bin"] = delta_bins.index / n_bins
  return delta_bins


# get the aboslute difference in assigned bin per item between the two dfs
def get_doi_bin_error_df(doi_bin_labels_a: pd.DataFrame, doi_bin_labels_b: pd.DataFrame):
  diff_df = pd.DataFrame(doi_bin_labels_a - doi_bin_labels_b, columns=["diff"]).abs()
  diff_df = diff_df.groupby("diff").size().reset_index()
  diff_df.columns = ["diff", "count"]
  return diff_df


def get_doi_error_df(doi_df_a: pd.DataFrame, doi_df_b: pd.DataFrame, absolute=True):
  if absolute:
    diff = pd.DataFrame(doi_df_a["doi"] - doi_df_b["doi"]).abs()
  else:
    diff = pd.DataFrame(doi_df_a["doi"] - doi_df_b["doi"])
  return diff
