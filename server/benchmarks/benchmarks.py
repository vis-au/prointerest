if True:
  import os
  from sys import path

  # make all files of the parent directory part of the path of this script, so that imports work
  # from notebooks and when running this script as __main__
  cwd = os.getcwd()
  path.append(f"{cwd}/..")

import json
from copy import copy
from test_case import *


PRESETS_PATH = "./presets.json"
TEST_CASES_PATH = "./test_cases.json"

DATASET_SUBDIR = "datasets"
DOI_SUBDIR = "doi"
PARAMETER_SUBDIR = "parameters"
STRATEGY_SUBDIR = "strategies"


# load a test case from test_cases.json and parse it into the TestCase format
def load_test_case(index: int, mode: str = None) -> TestCase:
  test_cases = get_all_test_cases()
  test_case_config = test_cases[index]
  doi_label = test_case_config["doi"]
  data_label = test_case_config["dataset"]
  parameter_label = test_case_config["parameters"]

  params_config = get_parameters_config(parameter_label)
  data_config = get_dataset_config(data_label)
  doi_config = get_doi_config(doi_label, data_config)

  s = test_case_config["storage_strategy"]
  u = test_case_config["update_strategy"]
  c = test_case_config["context_strategy"]
  strategy_config = get_strategy_config(c, u, s, params_config, data_config)
  name = strategy_config.name

  PATH = get_path(data_label, doi_label, params_config.total_size, params_config.chunk_size, mode)

  return create_test_case(
    name=name,
    strategies=strategy_config,
    data=data_config,
    doi=doi_config,
    params=params_config,
    path=PATH
  )


def get_all_test_cases():
  return json.load(open(TEST_CASES_PATH))["test_cases"]


def get_dataset_presets():
  return json.load(open(PRESETS_PATH))["datasets"]


def get_parameter_presets():
  return json.load(open(PRESETS_PATH))["parameters"]


def get_doi_function_presets():
  return json.load(open(PRESETS_PATH))["doi_functions"]


# load a test case with index _index_ from test_cases.json and run it
def run_test_case(index: int):
  tc = load_test_case(index)
  print(tc.name, tc.doi_csv_path)
  tc.run()
  print(f"done: {tc.pipeline.total_time}s")


# load test case with index __index__ from test_cases.json and run it in mixed mode
def run_test_case_mixed(index: int, mode: str = None):
  tc = load_test_case(index)
  tc.params.update_interval = 0  # update interval 0 --> mixed update, i.e., updates at every chunk
  tc.run()
  print(f"done: {tc.pipeline.total_time}s")


# load test case with index __index__ from test_cases.json and run its ground truth
def run_test_case_ground_truth(index: int, mode: str = None):
  tc = load_test_case(index)
  data = tc.data
  params = tc.params
  doi = tc.doi
  PATH = get_path(data.name, doi.name, params.total_size, params.chunk_size, mode)
  ground_truth_tc = create_ground_truth_test_case(tc.data, tc.doi, tc.params, PATH)
  print(ground_truth_tc.name, ground_truth_tc.doi_csv_path)
  ground_truth_tc.run()
  print(f"done: {ground_truth_tc.pipeline.total_time}s")


# load test case with index __index__ from test_cases.json, run it, and use all "space" for new data
def run_test_case_bigger_chunks(index: int, mode: str = None):
  tc = load_test_case(index)
  data = tc.data
  params = tc.params
  doi = tc.doi
  PATH = get_path(data.name, doi.name, params.total_size, params.chunk_size, mode)
  bigger_chunks_tc = create_bigger_chunks_test_case(tc.data, tc.doi, tc.params, PATH)
  print(bigger_chunks_tc.name, bigger_chunks_tc.doi_csv_path)
  bigger_chunks_tc.run()
  print(f"done: {bigger_chunks_tc.pipeline.total_time}s")


# n datasets : 1 parameter set : 1 doi : 1 set of strategies
def run_test_case_on_all_datasets(index: int, datasets: dict = None) -> None:
  datasets = get_dataset_presets() if datasets is None else datasets
  test_case = load_test_case(index, mode=DATASET_SUBDIR)

  i = 1
  for data_label in datasets:
    tc = copy(test_case)
    data_config = get_dataset_config(data_label)
    tc.data = data_config
    tc.name = f"{tc.name}-{data_label}"
    print(f"({i}/{len(datasets.keys())}): {test_case.name}")
    tc.run()
    print(f"done: {tc.pipeline.total_time}s")
    i += 1


# 1 dataset : n parameter sets : 1 doi : 1 set of strategies
def run_test_case_on_all_parameters(index: int, parameters: dict = None) -> None:
  parameters = get_parameter_presets() if parameters is None else parameters
  test_case = load_test_case(index, mode=PARAMETER_SUBDIR)

  i = 1
  for parameter_label in parameters:
    tc = copy(test_case)
    parameter_config = get_parameters_config(parameter_label)
    tc.params = parameter_config
    tc.name = f"{tc.name}-{parameter_label}"
    print(f"({i}/{len(parameters.keys())}): {test_case.name}")
    tc.run()
    print(f"done: {tc.pipeline.total_time}s")
    i += 1


# 1 dataset : 1 parameter set : n dois : 1 set of strategies
def run_test_case_on_all_doi_functions(index: int, doi_functions: list[str] = None) -> None:
  doi_functions = get_doi_function_presets() if doi_functions is None else doi_functions
  test_case = load_test_case(index, mode=DOI_SUBDIR)

  i = 1
  for doi_function in doi_functions:
    tc = copy(test_case)
    doi_config = get_doi_config(doi_function, tc.data)
    tc.doi = doi_config
    tc.name = f"{tc.name}-{doi_function}"
    print(f"({i}/{len(doi_functions.keys())}): {test_case.name}")
    tc.run()
    print(f"done: {tc.pipeline.total_time}s")
    i += 1


# 1 dataset : 1 parameter set : 1 doi : n sets of strategies
def run_test_case_for_all_strategies(index: int, all_storages: bool = False) -> None:
  tc = load_test_case(index, mode=STRATEGY_SUBDIR)

  contexts_, updates_, storages_ = generate_strategies(tc.data, tc.params)
  total_tcs = len(contexts_)*len(updates_)

  if all_storages:
    total_tcs *= len(storages_)
  else:
    storages_ = [s for s in storages_ if s[0] == "windowing"]

  print(f"data: {tc.data.name}, {get_short_title(tc.doi, tc.params)}\n####")

  completed_tcs = 0
  for c in contexts_:
    for u in updates_:
      for s in storages_:
        strategy_config = StrategiesConfiguration(
          name=f"{s[0]}-{u[0]}-{c[0]}" if all_storages else f"{u[0]}-{c[0]}",
          context_strategy=c[1](),
          update_strategy=u[1](),
          storage_strategy=s[1]()
        )
        tc_ = copy(tc)
        tc_.strategies = strategy_config
        tc_.name = strategy_config.name

        completed_tcs += 1
        print(f"({completed_tcs}/{total_tcs}): {tc_.name}")

        tc_.run()
        print(f"done: {tc_.pipeline.total_time}s")


# P datasets : Q parameter sets : R dois : S sets of strategies
def run_all_test_cases() -> None:
  n_test_cases = len(get_all_test_cases())

  for i in range(n_test_cases):
    run_test_case(i)
