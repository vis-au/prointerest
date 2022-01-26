if True:
  import os
  from sys import path

  # make this script "top level"
  cwd = os.getcwd()
  path.append(f"{cwd}/..")

import json
from test_case import (get_dataset_config, get_doi_config, get_parameters_config, get_path,
                       get_strategy_config, create_test_case)


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


tc_ = load_test_case(0)
print(tc_.name, tc_.doi_csv_path)
tc_.run()
