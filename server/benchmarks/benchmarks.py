if True:
  import os
  from sys import path

  # make this script "top level"
  cwd = os.getcwd()
  path.append(f"{cwd}/..")

import json
from copy import copy
from test_case import (get_dataset_config, get_doi_config, get_parameters_config, get_path,
                       get_strategy_config, create_test_case, generate_strategies,
                       StrategiesConfiguration)


def load_test_case(index: int):
  TEST_CASES = json.load(open("./test_cases.json"))
  test_case_config = TEST_CASES["test_cases"][index]
  doi_label = test_case_config["doi"]
  data_label = test_case_config["datasets"]
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

def run_single_test_case(index: int):
  tc = load_test_case(index)
  print(tc.name, tc.doi_csv_path)
  tc.run()


def run_test_case_for_all_strategies(index: int, all_storages: bool = False):
  tc = load_test_case(index)

  contexts_, updates_, storages_ = generate_strategies(tc.data, tc.params)
  total_tcs = len(contexts_)*len(updates_)

  if all_storages:
    total_tcs *= len(storages_)
  else:
    storages_ = [storages_[0]]  # first element is windowing strategy

  completed_tcs = 0
  for c in contexts_:
    for u in updates_:
      for s in storages_:
        strategy_config = StrategiesConfiguration(
          name=f"{s[0]}-{u[0]}-{c[0]}",
          context_strategy=c[1](),
          update_strategy=u[1](),
          storage_strategy=s[1]()
        )
        tc_ = copy(tc)
        tc_.strategies = strategy_config

        completed_tcs += 1
        print(f"({completed_tcs}/{total_tcs}): {tc_.name}")
        tc_.run()


# run_single_test_case(0)
run_test_case_for_all_strategies(0)
