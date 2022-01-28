from os.path import join
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


def get_strategy_bc_errors(path_list: list[str], file_name: str, label: str):
  strategies_error = pd.DataFrame()
  bigger_chunks_errors = pd.DataFrame()

  for test_case_path in path_list:
    if "ground_truth" in test_case_path or "bigger_chunks" in test_case_path:
      continue

    if label == "dois":
      test_case_label = test_case_path.split("/")[3]
    elif label == "datasets":
      test_case_label = test_case_path.split("/")[2]
    elif label == "parameters":
      test_case_label = "".join(test_case_path.split("/")[-3:-1])  # include data and chunk sizes

    df = pd.read_csv(join(test_case_path, file_name))
    gt = pd.read_csv(join(test_case_path, "__ground_truth__.csv"))
    bc = pd.read_csv(join(test_case_path, "__bigger_chunks__.csv"))

    strategy_error = get_doi_error_df(gt, df)
    strategy_error[label] = test_case_label
    strategies_error = strategies_error.append(strategy_error)
    strategies_error = strategies_error.append(strategy_error)

    bigger_chunks_error = get_doi_error_df(gt, bc)
    bigger_chunks_error[label] = test_case_label
    bigger_chunks_errors = bigger_chunks_errors.append(bigger_chunks_error)

  return strategies_error, bigger_chunks_errors
