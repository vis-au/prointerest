from time import time
from typing import final
from numpy import zeros_like
from pandas import DataFrame

from database import *
from doi_component.doi_component import *
from doi_component.outlierness_component import *
from context_item_selection_strategy.context_item_selection_strategy import *
from outdated_item_selection_strategy.outdated_item_selection_strategy import *


def reset():
  drop_tables()
  initialize_db("../data/nyc_taxis_sampled100k_shuffled.csv.gz")


class BenchmarkTestCaseStep():
  def __init__(self, step_number: int) -> None:
    self.step_number = step_number
    self.chunk_time = 0
    self.outdated_time = 0
    self.new_doi_time = 0
    self.old_doi_time = 0,
    self.store_new_time = 0
    self.update_dois_time = 0
    self.total_time = 0

  def __str__(self) -> str:
    return f"{self.step_number},{self.chunk_time},{self.outdated_time},{self.new_doi_time},"\
           f"{self.old_doi_time},{self.store_new_time},{self.update_dois_time},{self.total_time}"


class BenchmarkTestCase():
  def __init__(self, name: str, doi: DoiComponent, context_strategy: ContextItemSelectionStrategy,
               update_strategy: OutdatedItemSelectionStrategy, chunk_size: int, chunks: int):
    self.name = name
    self.doi = doi
    self.context_strategy = context_strategy
    self.update_strategy = update_strategy
    self.chunk_size = chunk_size
    self.chunks = chunks
    self.test_case_steps = []

  def __str__(self):
    output = "chunk,chunk_time,outdated_time,new_doi_time,old_doi_time,store_new_time,"\
             "update_dois_time,total_time\n"
    for step in self.test_case_steps:
      output = f"{output}{step}\n"
    return output

  def apply_test_case_strategy(self, chunk: DataFrame, chunk_no: int):
    new_ids = zeros_like(chunk)
    new_dois = zeros_like(chunk)
    new_bins = zeros_like(chunk)
    return new_ids, new_dois, new_bins

  @final
  def run(self):
    self.test_case_steps = []

    for i in range(self.chunks):
      step = BenchmarkTestCaseStep(i)
      step.total_time = time()

      now = time()
      chunk = get_next_chunk_from_db(self.chunk_size, as_df=True)
      step.chunk_time = time() - now

      # apply strategy for finding context items
      context = self.context_strategy.get_context_items(i)
      context = process_chunk(context)

      # apply strategy for finding outdated items
      now = time()
      outdated = self.update_strategy.get_outdated_items(current_chunk=i)
      outdated = process_chunk(pd.DataFrame(outdated))
      step.outdated_time = time() - now

      new_ids = chunk[ID].to_list()
      old_ids = outdated[ID].to_list()

      # compute the doi values for the chunk with context items
      now = time()
      chunk_with_context = chunk.append(context)
      new_doi = self.doi.compute_doi(chunk_with_context)[:len(chunk)]
      step.new_doi_time = time() - now

      # measure time for storing new values
      now = time()
      save_dois(new_ids, new_doi, np.zeros_like(new_doi))
      step.store_new_time = time() - now

      # update the doi values for outdated items
      now = time()
      chunk_with_outdated = chunk.append(outdated)
      old_doi = self.doi.compute_doi(chunk_with_outdated)[len(chunk):]
      step.old_doi_time = time() - now

      # measure time for updating values
      now = time()
      update_dois(old_ids, old_doi)
      step.update_dois_time = time() - now

      # measure total time
      step.total_time = time() - step.total_time
      self.test_case_steps += [step]

  def save(self, path=None):
    with open(f"{self.name}.csv", "w") as csv_file:
      csv_file.write(str(self))