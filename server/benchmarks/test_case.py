import os
import json
from dataclasses import dataclass, field

from database import initialize_db, drop_tables
from doi_components import get_doi_component
from progressive_doi_pipeline import ProgressiveDoiPipeline
from context_strategies import *
from update_strategies import *
from storage_strategies import *

from doi_component.doi_component import DoiComponent
from context_item_selection_strategy.context_item_selection_strategy import *
from context_item_selection_strategy.no_context import *
from outdated_item_selection_strategy.outdated_item_selection_strategy import *
from outdated_item_selection_strategy.no_update import *
from storage_strategy.storage_strategy import *
from storage_strategy.no_storage import NoStorage

PRESETS = json.load(open("./presets.json"))


@dataclass
class StrategiesConfiguration():
  name: str
  context_strategy: ContextItemSelectionStrategy
  update_strategy: OutdatedItemSelectionStrategy
  storage_strategy: StorageStrategy


@dataclass
class DatasetConfiguration():
  name: str
  data_path: str
  column_data_path: str
  id_column: str
  numeric_columns: list[str]  # columns used in the doi functions
  total_db_size: int  # full size of database
  n_dims: int  # number of dimensions in the data


@dataclass
class DoiConfiguration():
  name: str
  doi: DoiComponent = None


@dataclass
class ParametersConfiguration:
  name: str
  chunks: int  # number of steps
  total_size: int  # total number of processed items, not nec. the dataset size
  chunk_size: int  # number of new items retrieved per step
  context_size: int
  update_size: int
  storage_size: int  # maximum size of storages
  max_age: int  # maximal age of the considered chunks
  update_interval: int  # number of chunks before a full update occurs
  n_bins: int  # number of bins used in analysis


@dataclass
class TestCase:
  name: str
  strategies: StrategiesConfiguration
  data: DatasetConfiguration
  doi: DoiConfiguration
  params: ParametersConfiguration
  doi_csv_path: str = field(default_factory=lambda: None)
  times_csv_path: str = field(default_factory=lambda: None)
  pipeline: ProgressiveDoiPipeline = None

  def __copy__(self):
    return TestCase(
      self.name,
      self.strategies,
      self.data,
      self.doi,
      self.params,
      self.doi_csv_path,
      self.times_csv_path
    )

  def _generate_pipeline(self) -> ProgressiveDoiPipeline:
    return ProgressiveDoiPipeline(
      name=self.name,
      doi=self.doi.doi,
      storage_strategy=self.strategies.storage_strategy,
      context_strategy=self.strategies.context_strategy,
      update_strategy=self.strategies.update_strategy,
      chunk_size=self.params.chunk_size,
      context_size=self.params.context_size,
      update_size=self.params.update_size,
      chunks=self.params.chunks
    )

  def run(self, skip_if_exists: bool = True) -> None:
    self.initialize_database()
    self.pipeline = self._generate_pipeline()
    if skip_if_exists and os.path.isfile(f"{self.doi_csv_path}/{self.pipeline.name}.csv"):
      print("skipping test case because .csv file already exists")
      return self.pipeline
    self.pipeline.run(
      doi_csv_path=self.doi_csv_path,
      times_csv_path=self.times_csv_path,
      update_interval=self.params.update_interval
    )
    return self.pipeline

  # wipe the databases that track doi, processed, update chunks, etc.
  def initialize_database(self) -> None:
    drop_tables()
    initialize_db(
      row_data_path=self.data.data_path,
      column_data_path=self.data.column_data_path,
      id_column=self.data.id_column,
      total_size=self.data.total_db_size,
      process_chunk_callback=taxi_process_chunk if "taxis" in self.data.name else None
    )


def create_test_case(name: str, strategies: StrategiesConfiguration,
                     data: DatasetConfiguration, doi: DoiConfiguration,
                     params: ParametersConfiguration, path: str) -> TestCase:

  doi_csv_path = f"{path}/doi/"
  times_csv_path = f"{path}/times/"

  return TestCase(
    name=name,
    strategies=strategies,
    data=data,
    doi=doi,
    params=params,
    doi_csv_path=doi_csv_path,
    times_csv_path=times_csv_path
  )


def create_ground_truth_test_case(data: DatasetConfiguration, doi: DoiConfiguration,
                                  params: ParametersConfiguration, path: str) -> TestCase:

  s = NoStorage()
  name = "__ground_truth__"

  total_size = params.total_size

  strategy_config = StrategiesConfiguration(
    name=name,
    context_strategy=NoContext(data.n_dims, s),
    update_strategy=NoUpdate(data.n_dims, s),
    storage_strategy=s,
  )

  parameters_config = ParametersConfiguration(
    name=name,
    chunks=1,
    total_size=total_size,
    chunk_size=total_size,
    update_size=0,
    context_size=0,
    storage_size=0,
    max_age=0,
    update_interval=0,
    n_bins=params.n_bins
  )

  return create_test_case(
    name=name,
    strategies=strategy_config,
    data=data,
    doi=doi,
    params=parameters_config,
    path=path
  )


def create_bigger_chunks_test_case(data: DatasetConfiguration, doi: DoiConfiguration,
                                   params: ParametersConfiguration, path: str) -> TestCase:

  s = NoStorage()
  name = "__bigger_chunks__"

  strategy_config = StrategiesConfiguration(
    name=name,
    context_strategy=NoContext(data.n_dims, s),
    update_strategy=NoUpdate(data.n_dims, s),
    storage_strategy=s,
  )

  total_size = params.total_size
  chunk_size = params.chunk_size
  context_size = params.context_size
  update_size = params.update_size

  parameters_config = ParametersConfiguration(
    name=name,
    chunks=round(total_size // (chunk_size + context_size)),
    total_size=total_size,
    chunk_size=chunk_size + context_size,
    update_size=0,
    context_size=0,
    storage_size=0,
    max_age=0,
    update_interval=0,
    n_bins=params.n_bins
  )

  return create_test_case(
    name=name,
    strategies=strategy_config,
    data=data,
    doi=doi,
    params=parameters_config,
    path=path
  )


def get_dataset_config(data_label: str) -> DatasetConfiguration:
  preset = PRESETS["datasets"][data_label]
  rows_ = preset["data_path"]
  columns_ = preset["column_data_path"]
  data_size = preset["total_db_size"]
  n_dims = preset["n_dims"]
  numeric_ = preset["numeric_columns"]
  id_ = "tripID"  # TODO: static for now

  return DatasetConfiguration(data_label, rows_, columns_, id_, numeric_, data_size, n_dims)


def get_doi_config(doi_label: str, data: DatasetConfiguration) -> DoiConfiguration:
  doi_component = get_doi_component(doi_label, data.numeric_columns)

  return DoiConfiguration(doi_label, doi_component)


def get_parameters_config(parameter_label: str) -> ParametersConfiguration:
  preset = PRESETS["parameters"][parameter_label]
  total_size = preset["total_size"]
  chunk_size = preset["chunk_size"]
  chunks = round(total_size / chunk_size)
  context_size = preset["context_size"]
  update_size = preset["update_size"]
  max_age = preset["max_age"]
  storage_size = chunk_size * max_age
  update_interval = preset["update_interval"]
  n_bins = preset["n_bins"]

  return ParametersConfiguration(parameter_label, chunks, total_size, chunk_size, context_size,
                                 update_size, storage_size, max_age, update_interval, n_bins)


def get_strategy_config(context_label: str, update_label: str, storage_label: str,
                        params: ParametersConfiguration, data: DatasetConfiguration):
  context_ = get_context_strategy(context_label, data.n_dims, params.chunks, params.n_bins)
  update_ = get_update_strategy(update_label, data.n_dims, params.chunks, params.max_age,
                                params.n_bins)
  storage_ = get_storage_strategy(storage_label, params.max_age*params.chunk_size)

  return StrategiesConfiguration(
    name=f"{context_label}-{update_label}-{storage_label}",
    context_strategy=context_,
    update_strategy=update_,
    storage_strategy=storage_
  )


def generate_strategies(data: DatasetConfiguration, params: ParametersConfiguration):
  context_size = params.context_size
  chunk_size = params.context_size
  update_size = params.update_size
  storage_size = params.storage_size
  n_dims = data.n_dims
  n_bins = params.n_bins
  max_age = params.max_age
  total_size = params.total_size
  n_chunks_context = max(context_size // chunk_size, 1)  # number of chunks considered for context
  n_chunks_update = max(update_size // chunk_size, 1)  # number of chunks considered for updating

  context_strategies = get_context_strategies(n_dims, n_chunks_context, n_bins)
  update_strategies = get_update_strategies(n_dims, n_chunks_update, max_age, n_bins)
  storage_strategies = get_storage_strategies(storage_size)

  return context_strategies, update_strategies, storage_strategies


def get_short_title(doi: DoiConfiguration, params: ParametersConfiguration):
  return f"doi: {doi.name}, items: {params.total_size}, chunk size: {params.chunk_size}"


def get_full_title(doi: DoiConfiguration, params: ParametersConfiguration,
                   data: DatasetConfiguration):
  return f"{get_short_title(doi, params)}, data: {data.name},\n"\
          f"|upd.|.: {params.update_size}, |cont.|: {params.context_size},"\
          f"bins: {params.n_bins}, age: {params.max_age}\n"


def get_path(data_label: str, doi_label: str, total_size: int, chunk_size: int) -> str:

  path = f"./out/{data_label}/{doi_label}/{total_size}/{chunk_size}"

  if not os.path.exists("./out"):
    os.mkdir("./out")
  if not os.path.exists(f"./out/{data_label}"):
    os.mkdir(f"./out/{data_label}")
  if not os.path.exists(f"./out/{data_label}/{doi_label}"):
    os.mkdir(f"./out/{data_label}/{doi_label}")
  if not os.path.exists(f"./out/{data_label}/{doi_label}/{total_size}"):
    os.mkdir(f"./out/{data_label}/{doi_label}/{total_size}")
  if not os.path.exists(path):
    os.mkdir(path)

  return path


# compute the ratio and duration in s per ride in the taxi dataset
def taxi_process_chunk(chunk: pd.DataFrame):
  dropoff = chunk["tpep_dropoff_datetime"]
  pickup = chunk["tpep_pickup_datetime"]
  chunk["duration"] = dropoff - pickup
  chunk["duration"] = chunk["duration"].apply(lambda x: x.total_seconds())
  chunk["ratio"] = chunk["tip_amount"] / chunk["total_amount"]
  return chunk
