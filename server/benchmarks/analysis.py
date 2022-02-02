from os.path import join, exists
import json
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
def get_doi_delta_bins_df(doi_bins_a: pd.DataFrame, doi_bins_b: pd.DataFrame):
  # copy the first df
  delta_bins = pd.DataFrame(doi_bins_a)
  delta_bins["delta"] = (doi_bins_a[0] - doi_bins_b[0])
  delta_bins.columns = ["doi", "delta"]
  delta_bins["bin"] = delta_bins.index
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


def get_strategy_bc_errors(path_list: list[str], file_name: str, label: str,
                           absolute: bool = False, no_strategies: bool = False):
  strategy_errors = pd.DataFrame()
  bigger_chunks_errors = pd.DataFrame()
  no_strategies_errors = pd.DataFrame()

  for test_case_path in path_list:
    if "ground_truth" in test_case_path or "bigger_chunks" in test_case_path:
      continue

    # remove the file name
    test_case_path = test_case_path.split(file_name)[0]

    if label == "dois":
      test_case_label = test_case_path.split("/")[3]
    elif label == "datasets":
      test_case_label = test_case_path.split("/")[2]
    elif label == "parameters":
      test_case_label = "".join(test_case_path.split("/")[-3:-1])  # include data and chunk sizes
    else:
      raise Exception("please use either of [dois, datasets, parameters] as label")

    # check if the files exist before loading them
    if not exists(join(test_case_path, file_name)):
      print("skipping", join(test_case_path, file_name))
      continue
    df = pd.read_csv(join(test_case_path, file_name))

    if not exists(join(test_case_path, "__bigger_chunks__.csv")):
      continue
    bc = pd.read_csv(join(test_case_path, "__bigger_chunks__.csv"))

    if not exists(join(test_case_path, "__no_strategies__.csv")):
      continue
    sc = pd.read_csv(join(test_case_path, "__no_strategies__.csv"))

    if not exists(join(test_case_path, "__ground_truth__.csv")):
      continue
    gt = pd.read_csv(join(test_case_path, "__ground_truth__.csv"))

    strategy_error = get_doi_error_df(gt, df, absolute=absolute)
    strategy_error[label] = test_case_label
    strategy_errors = strategy_errors.append(strategy_error)

    bigger_chunks_error = get_doi_error_df(gt, bc, absolute=absolute)
    bigger_chunks_error[label] = test_case_label
    bigger_chunks_errors = bigger_chunks_errors.append(bigger_chunks_error)

    no_strategies_error = get_doi_error_df(gt, sc, absolute=absolute)
    no_strategies_error[label] = test_case_label
    no_strategies_errors = no_strategies_errors.append(no_strategies_error)

  if no_strategies:
    return strategy_errors, bigger_chunks_errors, no_strategies_errors
  else:
    return strategy_errors, bigger_chunks_errors


def get_error_for_test_case(test_case_file_name: str, mode: str):
  selected_test_case = json.load(open("./out/"+test_case_file_name))
  test_cases = selected_test_case["test_cases"]
  test_case_doi_paths = [tc["dois_path"] for tc in test_cases]

  context_strategies = np.unique([tc["context_strategy"] for tc in test_cases]).tolist()
  update_strategies = np.unique([tc["update_strategy"] for tc in test_cases]).tolist()
  storage_strategies = np.unique([tc["storage_strategy"] for tc in test_cases]).tolist()

  all_strategies_error = pd.DataFrame()
  all_bigger_chunks_error = pd.DataFrame()
  all_no_strategies_error = pd.DataFrame()

  for c in context_strategies:
    for u in update_strategies:
      for s in storage_strategies:
        file_name = f"{c}-{u}-{s}.csv"
        strategies_error, bc_error, sc_error = get_strategy_bc_errors(
          path_list=[p for p in test_case_doi_paths if file_name in p],
          file_name=file_name,
          label=mode,
          absolute=False,
          no_strategies=True
        )
        strategies_error["context_strategy"] = c
        strategies_error["update_strategy"] = u
        strategies_error["storage_strategy"] = s

        bc_error["context_strategy"] = c
        bc_error["update_strategy"] = u
        bc_error["storage_strategy"] = s

        sc_error["context_strategy"] = c
        sc_error["update_strategy"] = u
        sc_error["storage_strategy"] = s

        all_strategies_error = all_strategies_error.append(strategies_error)
        all_bigger_chunks_error = all_bigger_chunks_error.append(bc_error)
        all_no_strategies_error = all_no_strategies_error.append(sc_error)

        # mean_strategy_error = strategies_error.groupby([mode]).mean().reset_index()
        # mean_bc_error = bigger_chunks_errors.groupby([mode]).mean().reset_index()
        # strategy_errors = strategy_errors.append(mean_strategy_error)
        # bigger_chunk_errors = bigger_chunk_errors.append(mean_bc_error)
  return all_strategies_error, all_bigger_chunks_error, all_no_strategies_error


def merge_err_dfs(strat_err_df: pd.DataFrame, bc_err_df: pd.DataFrame, mode: str):
  df = strat_err_df
  df["_doi_"] = bc_err_df["doi"].to_numpy()

  columns = [mode, "context_strategy", "update_strategy", "storage_strategy"]

  df_a = df[["doi"] + columns]
  df_b = df[["_doi_"] + columns]
  df_b = df_b.rename(columns={"_doi_": "doi"})
  df_a["type"] = "using strategies"
  df_b["type"] = "using bigger chunks"
  df = df_a.append(df_b)
  df.reset_index(inplace=True)

  return df
