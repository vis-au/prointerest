from os import mkdir
from os.path import exists
from pandas import DataFrame
from time import time
from typing import final

from database import *
from doi_component.doi_component import *
from storage_strategy.storage_strategy import *
from context_item_selection_strategy.context_item_selection_strategy import *
from outdated_item_selection_strategy.outdated_item_selection_strategy import *
from outdated_item_selection_strategy.no_update import NoUpdate


class DoiComputationTimeStep():
  def __init__(self, step_number: int) -> None:
    self.step_number = step_number
    self.step_time = 0  # time to do all steps in the computation
    self.chunk_time = 0  # time to retrieve the data
    self.storage_time = 0  # time to save the data
    self.context_time = 0  # time to retrieve context data
    self.update_context_dois_time = 0  # time to update context dois
    self.outdated_time = 0  # time to retrieve outdated data
    self.new_doi_time = 0  # time to compute the new doi values
    self.old_doi_time = 0  # time to recompute the outdated doi values
    self.store_new_time = 0  # time to store the new doi values
    self.update_dois_time = 0  # time to update the stored outdated values

  def __str__(self) -> str:
    return f"{self.step_number},{self.chunk_time},{self.storage_time},{self.context_time},"\
           f"{self.update_context_dois_time},{self.outdated_time},{self.new_doi_time},"\
           f"{self.old_doi_time},{self.store_new_time},{self.update_dois_time},{self.step_time}"


class ProgressiveDoiPipeline():
  def __init__(self, name: str, doi: DoiComponent, storage_strategy: StorageStrategy,
               context_strategy: ContextItemSelectionStrategy,
               update_strategy: OutdatedItemSelectionStrategy, chunk_size: int, chunks: int,
               context_size: int = 0, update_size: int = 0):
    self.name = name
    self.doi = doi

    self.storage_strategy = storage_strategy
    self.context_strategy = context_strategy
    self.update_strategy = update_strategy
    self.context_strategy.storage = self.storage_strategy
    self.update_strategy.storage = self.storage_strategy

    self.chunk_size = chunk_size
    self.context_size = context_size
    self.update_size = update_size
    self.chunks = chunks
    self.test_case_steps = []

    self.total_time = -1  # negative value indicates that the test case has not been run, yet
    self.times_csv_path = None  # set once this test case is run
    self.doi_csv_path = None  # set once this test case is run

  def __str__(self):
    output = "step,chunk_time,storage_time,context_time,update_context_dois_time,outdated_time,"\
             "new_doi_time,old_doi_time,store_new_time,update_dois_time,step_time\n"
    for step in self.test_case_steps:
      output = f"{output}{step}\n"
    return output

  def _apply_context_strategy(self, chunk: DataFrame, step: DoiComputationTimeStep):
    # apply strategy for finding context items
    now = time()
    context = self.context_strategy.get_context_items(
      n=self.context_size,
      current_chunk=step.step_number
    )
    context = process_chunk(context)
    step.context_time = time() - now

    # compute the doi values for the chunk with context items
    now = time()
    chunk_with_context = chunk.append(context)
    doi = self.doi.compute_doi(chunk_with_context)
    new_doi = doi[:len(chunk)]
    step.new_doi_time = time() - now

    # get the current doi values for the context and add the newly computed doi as mean
    now = time()
    if len(context) > 0:
      new_context_doi = doi[len(chunk):]
      context_ids = context[ID]
      context_ids = context_ids.tolist()
      old_context_doi = get_dois(context_ids).astype(np.float)
      updated_context_doi = (new_context_doi + old_context_doi) / 2
      update_dois(context_ids, updated_context_doi)
    step.update_context_doi_time = time() - now

    # measure time for storing new values
    new_ids = chunk[ID].to_list()
    now = time()
    save_dois(new_ids, new_doi)
    step.store_new_time = time() - now

  def _apply_update_strategy(self, chunk: DataFrame, step: DoiComputationTimeStep):
    # apply strategy for finding outdated items
    now = time()
    outdated = self.update_strategy.get_outdated_items(
      n=self.update_size,
      current_chunk=step.step_number
    )
    outdated = process_chunk(DataFrame(outdated))
    step.outdated_time = time() - now

    if len(outdated) == 0:
      step.old_doi_time = 0
      step.update_dois_time = 0
      return

    # recompute the doi values for outdated items
    now = time()
    chunk_with_outdated = chunk.append(outdated)
    new_outdated_doi = self.doi.compute_doi(chunk_with_outdated)[len(chunk):]
    step.old_doi_time = time() - now

    # measure time for updating values
    outdated_ids = outdated[ID].to_list()
    now = time()
    old_outdated_doi = get_dois(outdated_ids).astype(np.float)
    updated_context_doi = (new_outdated_doi + old_outdated_doi) / 2
    update_dois(outdated_ids, updated_context_doi)
    step.update_dois_time = time() - now

  def _get_next_chunk(self, n: int, step: DoiComputationTimeStep):
    # measure data retrieval time
    now = time()
    chunk = get_next_chunk_from_db(n, as_df=True)
    step.chunk_time = time() - now
    return chunk

  def _insert_into_storage(self, chunk: DataFrame, step: DoiComputationTimeStep):
    # measure inserting into storage time
    now = time()
    self.storage_strategy.insert_chunk(chunk, step.step_number)
    step.storage_time = time() - now

  def _run_next_synchronous_step(self, update_interval: int, processed_items: int,
                                 step: DoiComputationTimeStep):
    step.step_time = time()
    n_unprocessed_items = self.chunk_size*self.chunks - processed_items

    if step.step_number % update_interval == 0 and not isinstance(self.update_strategy, NoUpdate):
      # update as much data as possible without retrieving any new data
      now = time()
      n = min(self.update_size, n_unprocessed_items)
      chunk = self.update_strategy.get_outdated_items(n=n, current_chunk=step.step_number)
      chunk = process_chunk(DataFrame(chunk))
      step.outdated_time = time() - now
      now = time()
      if len(chunk) > 0:
        doi = self.doi.compute_doi(chunk)
        update_dois(chunk[ID].to_list(), doi)
      step.old_doi_time = time() - now
    else:
      # process the next chunk without an update
      n = min(self.chunk_size, n_unprocessed_items)
      chunk = self._get_next_chunk(n, step)
      processed_items += n

      # compute doi using the strategies
      self._apply_context_strategy(chunk, step)

      # measure inserting into storage time
      self._insert_into_storage(chunk, step)

    step.step_time = time() - step.step_time
    return processed_items

  def _run_synchronously(self, update_interval: int):
    self.test_case_steps = []
    start_time = time()

    processed_items = 0
    i = 0
    while processed_items < self.chunk_size*self.chunks:
      # run an update, using as much data as possible without retrieving any new data
      i += 1
      step = DoiComputationTimeStep(i)
      processed_items = self._run_next_synchronous_step(update_interval, processed_items, step)
      self.test_case_steps += [step]

    # measure test case time
    self.total_time = time() - start_time

  def _run_next_mixed_step(self, step: DoiComputationTimeStep):
    step.step_time = time()

    chunk = self._get_next_chunk(self.chunk_size, step)

    # compute the doi function given the strategies
    self._apply_context_strategy(chunk, step)
    self._apply_update_strategy(chunk, step)

    # measure inserting into storage time
    self._insert_into_storage(chunk, step)

    # measure step time
    step.step_time = time() - step.step_time
    return step

  def _run_mixed(self):
    self.test_case_steps = []
    start_time = time()

    for i in range(self.chunks):
      step = DoiComputationTimeStep(i)
      self._run_next_mixed_step(step)
      self.test_case_steps += [step]

    # measure test case time
    self.total_time = time() - start_time

  @final
  def run(self, doi_csv_path: str = None, times_csv_path: str = None, update_interval: int = 0):
    if update_interval > 0:
      self._run_synchronously(update_interval)
    else:
      self._run_mixed()

    self.save_doi(doi_csv_path)
    self.save_times(times_csv_path)

  # write the doi values computed by this combination of strategies to a csv file for later analysis
  def save_doi(self, path: str):
    if path is None:
      return

    if not exists(path):
      mkdir(path)
    get_from_doi(["TRUE"], as_df=True).to_csv(f"{path}/{self.name}.csv", index=False)

  # write benchmarking times to a csv file for later analysis
  def save_times(self, path: str):
    if path is None:
      return

    if not exists(path):
      mkdir(path)
    with open(f"{path}/{self.name}.csv", "w") as csv_file:
      csv_file.write(str(self))
