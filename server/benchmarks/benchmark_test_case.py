from os import mkdir
from os.path import exists
from pandas import DataFrame, read_csv
from time import time
from typing import final

from database import *
from doi_component.doi_component import *
from doi_component.outlierness_component import *
from context_item_selection_strategy.context_item_selection_strategy import *
from outdated_item_selection_strategy.outdated_item_selection_strategy import *


class BenchmarkTestCaseStep():
  def __init__(self, step_number: int) -> None:
    self.step_number = step_number
    self.step_time = 0
    self.chunk_time = 0
    self.context_time = 0
    self.outdated_time = 0
    self.new_doi_time = 0
    self.old_doi_time = 0,
    self.store_new_time = 0
    self.update_dois_time = 0

  def __str__(self) -> str:
    return f"{self.step_number},{self.chunk_time},{self.context_time},{self.outdated_time},"\
           f"{self.new_doi_time},{self.old_doi_time},{self.store_new_time},"\
           f"{self.update_dois_time},{self.step_time}"


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

    self.total_time = -1  # negative value indicates that the test case has not been run, yet
    self.times_csv_path = None  # set once this test case is run
    self.doi_csv_path = None  # set once this test case is run

  def __str__(self):
    output = "chunk,chunk_time,context_time,outdated_time,new_doi_time,old_doi_time,"\
             "store_new_time,update_dois_time,total_time\n"
    for step in self.test_case_steps:
      output = f"{output}{step}\n"
    return output

  def _apply_context_strategy(self, chunk: DataFrame, step: BenchmarkTestCaseStep, step_no: int):
    # apply strategy for finding context items
    now = time()
    context = self.context_strategy.get_context_items(current_chunk=step_no)
    context = process_chunk(context)
    step.context_time = time() - now

    # compute the doi values for the chunk with context items
    now = time()
    chunk_with_context = chunk.append(context)
    new_doi = self.doi.compute_doi(chunk_with_context)[:len(chunk)]
    step.new_doi_time = time() - now

    # measure time for storing new values
    new_ids = chunk[ID].to_list()
    now = time()
    save_dois(new_ids, new_doi, np.zeros_like(new_doi))
    step.store_new_time = time() - now

  def _apply_update_strategy(self, chunk: DataFrame, step: BenchmarkTestCaseStep, step_no: int):
    # apply strategy for finding outdated items
    now = time()
    outdated = self.update_strategy.get_outdated_items(current_chunk=step_no)
    outdated = process_chunk(DataFrame(outdated))
    step.outdated_time = time() - now

    if len(outdated) == 0:
      step.old_doi_time = 0
      step.update_dois_time = 0
      return

    # update the doi values for outdated items
    now = time()
    chunk_with_outdated = chunk.append(outdated)
    old_doi = self.doi.compute_doi(chunk_with_outdated)[len(chunk):]
    step.old_doi_time = time() - now

    # measure time for updating values
    old_ids = outdated[ID].to_list()
    now = time()
    update_dois(old_ids, old_doi)
    step.update_dois_time = time() - now

  @final
  def run(self, doi_csv_path=None, times_csv_path=None):
    self.test_case_steps = []
    start_time = time()

    for i in range(self.chunks):
      step = BenchmarkTestCaseStep(i)
      step.step_time = time()

      # measure data retrieval time
      now = time()
      chunk = get_next_chunk_from_db(self.chunk_size, as_df=True)
      step.chunk_time = time() - now

      # compute doi using the strategies
      self._apply_context_strategy(chunk, step, i)
      self._apply_update_strategy(chunk, step, i)

      # measure step time
      step.step_time = time() - step.step_time
      self.test_case_steps += [step]

    # measure test case time
    self.total_time = time() - start_time

    # write the doi values computed by this combination of strategies to a csv file for later
    # analysis
    if doi_csv_path:
      self.doi_csv_path = doi_csv_path
      if not exists(doi_csv_path):
        mkdir(doi_csv_path)
      get_from_doi(["TRUE"], as_df=True).to_csv(f"{doi_csv_path}/{self.name}.csv", index=False)

    # write benchmarking times to a csv file for later analysis
    if times_csv_path:
      self.times_csv_path = times_csv_path
      if not exists(times_csv_path):
        mkdir(times_csv_path)
      with open(f"{times_csv_path}/{self.name}.csv", "w") as csv_file:
        csv_file.write(str(self))

  def doi_histogram(self, bins=10):
    if not self.doi_csv_path:
      raise Exception("No CSV file for DOI values found. Supply a path during run().")
    df = read_csv(self.doi_csv_path)
    df.hist(column=DOI, bins=bins)

  def times_linecharts(self):
    if not self.times_csv_path:
      raise Exception("No CSV file for times found. Supply a path during run().")
    df = read_csv(self.times_csv_path)
    # TODO: render line charts, with one line per measured time in the test_case
