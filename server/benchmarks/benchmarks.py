if True:
  import os
  from sys import path

  # make all files of the parent directory part of the path of this script, so that imports work
  # from notebooks and when running this script as __main__
  cwd = os.getcwd()
  path.append(f"{cwd}/..")

from fileinput import filename
import json
import os
from datetime import datetime
from copy import copy
from typing import Literal
from test_case import *


STATE = Literal["single", "bigger_chunks", "ground_truth"]

PRESETS_PATH = "./presets.json"
TEST_CASES_PATH = "./test_cases.json"
MODES = ["datasets", "dois", "parameters", "strategies"]  # order same as order in doi.csv paths


# load a test case from test_cases.json and parse it into the TestCase format
def load_test_case(index: int) -> TestCase:
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

  PATH = get_path(data_label, doi_label, params_config.total_size, params_config.chunk_size)

  return create_test_case(
    name=name,
    strategies=strategy_config,
    data=data_config,
    doi=doi_config,
    params=params_config,
    path=PATH
  )


# load all combinations of test cases defined in a test_case in test_case.json into TestCases
def load_composite_test_cases(index: int) -> tuple[list[TestCase], list[str]]:
  test_cases = get_all_composite_test_cases()
  test_case_config = test_cases[index]

  dois = test_case_config["dois"]
  datasets = test_case_config["datasets"]
  parameters = test_case_config["parameters"]
  context_strategies = test_case_config["context_strategies"]
  update_strategies = test_case_config["update_strategies"]
  storage_strategies = test_case_config["storage_strategies"]

  tcs: list[TestCase] = []
  labels: list[str] = []

  for doi_label in dois:
    for data_label in datasets:
      for param_label in parameters:
        for c in context_strategies:
          for u in update_strategies:
            for s in storage_strategies:
              para_config = get_parameters_config(param_label)
              data_config = get_dataset_config(data_label)
              doi_config = get_doi_config(doi_label, data_config)

              strategy_config = get_strategy_config(c, u, s, para_config, data_config)
              name = strategy_config.name

              PATH = get_path(data_label, doi_label, para_config.total_size, para_config.chunk_size)

              tcs += [create_test_case(
                name=name,
                strategies=strategy_config,
                data=data_config,
                doi=doi_config,
                params=para_config,
                path=PATH
              )]
              labels += [[doi_label, data_label, param_label, c, u, s]]
  return tcs, labels


def get_all_test_cases():
  return json.load(open(TEST_CASES_PATH))["test_cases"]


def get_all_composite_test_cases():
  return json.load(open(TEST_CASES_PATH))["composite_test_cases"]


def get_dataset_presets():
  return json.load(open(PRESETS_PATH))["datasets"]


def get_parameter_presets():
  return json.load(open(PRESETS_PATH))["parameters"]


def get_doi_function_presets():
  return json.load(open(PRESETS_PATH))["doi_functions"]


def run_test_case_config(index: int):
  tc = load_test_case(index)
  print(tc.name, tc.doi_csv_path)
  tc.run()
  print(f"done: {tc.pipeline.total_time}s")
  return tc


# load test case with index __index__ from test_cases.json and run it in mixed mode
def run_test_case_mixed(index: int):
  tc = load_test_case(index)
  tc.params.update_interval = 0  # update interval 0 --> mixed update, i.e., updates at every chunk
  tc.run()
  print(f"done: {tc.pipeline.total_time}s")
  return tc


def get_variant_for_variables(index: int, variables: list[str],
                              apply_variable: Callable[[TestCase, str], TestCase],
                              state: STATE = "single") -> list[TestCase]:
  variants: list[TestCase] = []
  i = 1
  for variable in variables:
    tc = load_test_case(index)
    tc = apply_variable(tc, variable)
    tc.name = f"{tc.name}"
    params = tc.params
    doi = tc.doi
    data = tc.data
    p = get_path(data.name, doi.name, params.total_size, params.chunk_size)
    tc.doi_csv_path = f"{p}/doi/"
    tc.times_csv_path = f"{p}/times/"

    if state == "bigger_chunks":
      tc = transform_into_bigger_chunks_test_case(tc)
    elif state == "ground_truth":
      tc = transform_into_ground_truth_test_case(tc)

    variants += [tc]
    i += 1
  return variants


def get_variant_for_all_datasets(index: int, datasets: dict,
                                 state: STATE = "single") -> list[TestCase]:
  def callback(tc: TestCase, data_label: str):
    data_config = get_dataset_config(data_label)
    tc.data = data_config
    tc.doi = get_doi_config(tc.doi.name, tc.data)
    return tc

  data_labels = datasets.keys()
  variants = get_variant_for_variables(
    index, data_labels, apply_variable=callback, state=state
  )

  return variants


def get_variant_for_all_parameters(index: int, parameters: dict,
                                   state: STATE = "single") -> list[TestCase]:
  def callback(tc: TestCase, parameter_label: str):
    parameter_config = get_parameters_config(parameter_label)
    tc.params = parameter_config
    return tc

  params = parameters.keys()
  variants = get_variant_for_variables(
    index, params, apply_variable=callback, state=state
  )

  return variants


def get_variant_for_all_doi_functions(index: int, dois: list[str],
                                      state: STATE = "single") -> list[TestCase]:
  def callback(tc: TestCase, doi_function: str):
    doi_config = get_doi_config(doi_function, tc.data)
    tc.doi = doi_config
    return tc

  variants = get_variant_for_variables(
    index, dois, apply_variable=callback, state=state
  )

  return variants


def get_variant_for_all_strategies(index: int, all_storages: bool = False) -> list[TestCase]:
  tc = load_test_case(index)
  contexts_, updates_, storages_ = generate_strategies(tc.data, tc.params)

  contexts_, updates_, storages_ = generate_strategies(tc.data, tc.params)
  total_tcs = len(contexts_)*len(updates_)

  if all_storages:
    total_tcs *= len(storages_)
  else:
    storages_ = [s for s in storages_ if s[0] == "windowing"]

  variants: list[TestCase] = []
  i = 0
  for c in contexts_:
    for u in updates_:
      for s in storages_:
        tc_ = load_test_case(index)
        strategy_config = StrategiesConfiguration(
          name=f"{s[0]}-{u[0]}-{c[0]}" if all_storages else f"{u[0]}-{c[0]}",
          context_strategy=c[1](),
          update_strategy=u[1](),
          storage_strategy=s[1]()
        )
        tc_.strategies = strategy_config
        tc_.name = strategy_config.name

        i += 1
        variants += [tc_]
  return variants


def transform_into_ground_truth_test_case(test_case: TestCase):
  data = test_case.data
  params = test_case.params
  doi = test_case.doi
  PATH = get_path(data.name, doi.name, params.total_size, params.chunk_size)

  return create_ground_truth_test_case(data, doi, params, PATH)


def transform_into_no_strategy_test_case(test_case: TestCase):
  data = test_case.data
  params = test_case.params
  doi = test_case.doi
  PATH = get_path(data.name, doi.name, params.total_size, params.chunk_size)

  return create_no_strategy_test_case(data, doi, params, PATH)


def transform_into_bigger_chunks_test_case(test_case: TestCase):
  data = test_case.data
  params = test_case.params
  doi = test_case.doi
  PATH = get_path(data.name, doi.name, params.total_size, params.chunk_size)

  return create_bigger_chunks_test_case(data, doi, params, PATH)


def save_benchmark_run(test_cases: list[TestCase], index: int, mode: str):
  tcs = [
    {
      "dataset": tc.data.name,
      "doi": tc.doi.name,
      "parameters": tc.params.name,
      "context_strategy": tc.name.split("-")[0],
      "update_strategy": tc.name.split("-")[1],
      "storage_strategy": tc.name.split("-")[2],
      "dois_path": f"{tc.doi_csv_path}{tc.name}.csv",
      "times_path": f"{tc.times_csv_path}{tc.name}.csv"
    } for tc in test_cases
  ]
  now = str(datetime.now())
  run = {
    "timestamp": now,
    "preset_index": index,
    "mode": mode,
    "test_cases": tcs,
  }
  run_json = json.dumps(run, indent=2)

  if not os.path.exists("./out/"):
    os.mkdir("./out/")

  filename = f"test case {index} - {mode}"
  with open(f"./out/{filename}.json", "w") as file:
    file.write(run_json)


# n datasets : 1 parameter set : 1 doi : 1 set of strategies
def run_test_case_on_all_datasets(index: int, datasets: dict = None,
                                  state: STATE = "single") -> None:
  datasets = get_dataset_presets() if datasets is None else datasets
  variants = get_variant_for_all_datasets(index, datasets, state)

  for i, variant in enumerate(variants):
    print(f"({i}/{len(datasets.keys())}): {variant.name}")
    variant.run()
    print(f"done: {variant.pipeline.total_time}s")

  return variants


# 1 dataset : n parameter sets : 1 doi : 1 set of strategies
def run_test_case_on_all_parameters(index: int, parameters: dict = None,
                                    state: STATE = "single") -> None:
  parameters = get_parameter_presets() if parameters is None else parameters
  variants = get_variant_for_all_parameters(index, parameters, state)

  for i, variant in enumerate(variants):
    print(f"({i}/{len(parameters.keys())}): {variant.name}")
    variant.run()
    print(f"done: {variant.pipeline.total_time}s")

  return variants


# 1 dataset : 1 parameter set : n dois : 1 set of strategies
def run_test_case_on_all_doi_functions(index: int, doi_functions: list[str] = None,
                                       state: STATE = "single") -> None:

  doi_functions = get_doi_function_presets() if doi_functions is None else doi_functions
  variants = get_variant_for_all_doi_functions(index, doi_functions, state)

  for i, variant in enumerate(variants):
    print(f"({i}/{len(doi_functions)}): {variant.name}")
    variant.run()
    print(f"done: {variant.pipeline.total_time}s")

  return variants


# 1 dataset : 1 parameter set : 1 doi : n sets of strategies
def run_test_case_on_all_strategies(index: int, all_storages: bool = False) -> None:
  tc = load_test_case(index)

  print(f"data: {tc.data.name}, {get_short_title(tc.doi, tc.params)}\n####")

  variants = get_variant_for_all_strategies(index, all_storages)
  for i, variant in enumerate(variants):
    print(f"({i}/{len(variants)}): {variant.name}")
    variant.run()
    print(f"done: {variant.pipeline.total_time}s")
  return variants


# P datasets : Q parameter sets : R dois : S sets of strategies
def run_all_test_case_configs() -> None:
  n_test_cases = len(get_all_test_cases())
  tcs: list[TestCase] = []
  for i in range(n_test_cases):
    tc = run_test_case_config(i)
    tcs += [tc]
  return tcs


# load a test case with index _index_ from test_cases.json and run it
def run_test_case(index: int, mode: str = None) -> None:
  if mode == "composite":
    tcs = run_composite_test_case(index)
  elif mode == "strategies":
    tcs = run_test_case_on_all_strategies(index)
  elif mode == "dois":
    tcs = run_test_case_on_all_doi_functions(index)
  elif mode == "datasets":
    tcs = run_test_case_on_all_datasets(index)
  elif mode == "parameters":
    tcs = run_test_case_on_all_parameters(index)
  else:
    tcs = run_test_case_config(index)
    mode = "default"  # used for filename when saving

  save_benchmark_run(tcs, index, mode)


def run_composite_test_case(index: int) -> None:
  variants, labels = load_composite_test_cases(index)

  for i, variant in enumerate(variants):
    print(f"\n({i}/{len(variants)}): {variant.name}")
    print(f"{' : '.join(labels[i])}")
    variant.run()
    print(f"done: {variant.pipeline.total_time}s")

    bc = transform_into_bigger_chunks_test_case(variant)
    sc = transform_into_no_strategy_test_case(variant)
    gt = transform_into_ground_truth_test_case(variant)
    print("ground truth")
    gt.run()
    print(f"done: {gt.pipeline.total_time}s")
    print("smaller chunks")
    sc.run()
    print(f"done {sc.pipeline.total_time}s")
    print("bigger chunks")
    bc.run()
    print(f"done: {bc.pipeline.total_time}s")

  return variants


# load test case with index __index__ from test_cases.json and run its ground truth
def run_test_case_ground_truth(index: int, mode: str = None) -> None:
  if mode == "dois":
    run_test_case_on_all_doi_functions(index, state="ground_truth")
  elif mode == "datasets":
    run_test_case_on_all_datasets(index, state="ground_truth")
  elif mode == "parameters":
    run_test_case_on_all_parameters(index, state="ground_truth")
  else:
    tc = load_test_case(index)
    ground_truth_tc = transform_into_ground_truth_test_case(tc)
    print(ground_truth_tc.name, ground_truth_tc.doi_csv_path)
    ground_truth_tc.run()
    print(f"done: {ground_truth_tc.pipeline.total_time}s")


# load test case with index __index__ from test_cases.json, run it, and use all "space" for new data
def run_test_case_no_strategies(index: int, mode: str = None) -> None:
  if mode == "dois":
    run_test_case_on_all_doi_functions(index, state="no_strategies")
  elif mode == "datasets":
    run_test_case_on_all_datasets(index, state="no_strategies")
  elif mode == "parameters":
    run_test_case_on_all_parameters(index, state="no_strategies")
  else:
    tc = load_test_case(index)
    no_strategies_tc = transform_into_no_strategy_test_case(tc)
    print(no_strategies_tc.name, no_strategies_tc.doi_csv_path)
    no_strategies_tc.run()
    print(f"done: {no_strategies_tc.pipeline.total_time}s")


# load test case with index __index__ from test_cases.json, run it, and use all "space" for new data
def run_test_case_bigger_chunks(index: int, mode: str = None) -> None:
  if mode == "dois":
    run_test_case_on_all_doi_functions(index, state="bigger_chunks")
  elif mode == "datasets":
    run_test_case_on_all_datasets(index, state="bigger_chunks")
  elif mode == "parameters":
    run_test_case_on_all_parameters(index, state="bigger_chunks")
  else:
    tc = load_test_case(index)
    bigger_chunks_tc = transform_into_bigger_chunks_test_case(tc)
    print(bigger_chunks_tc.name, bigger_chunks_tc.doi_csv_path)
    bigger_chunks_tc.run()
    print(f"done: {bigger_chunks_tc.pipeline.total_time}s")


if __name__ == "__main__":
  import sys
  if len(sys.argv) == 1:
    raise Exception("please provide the index of a test case from test_case.json and, optionally, "
                    "an execution mode.")
  else:
    if len(sys.argv) == 2:
      try:
        isinstance(int(sys.argv[1]), int)  # throws an error if argv[1] is not an integer
        run_test_case(sys.argv[1])
      except ValueError:
        if sys.argv[1].lower() == "all":
          run_all_test_case_configs()
        else:
          raise Exception("make sure the first parameter you provide is an integer or 'all'.")
    else:
      run_test_case(index=int(sys.argv[1]), mode=sys.argv[2])
