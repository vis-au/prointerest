import duckdb
import numpy as np
import pandas as pd
import random
from typing import Callable, List

# TOTAL_SIZE = 112145904
TOTAL_SIZE: int = None

# database constants
# path to the (compressed) data file in row-based format
# PATH = "./data/nyc_taxis.shuffled_full.csv.gz"
PATH: str = None

# path to the (compressed) data file in column-based format
# PATH_COLUMN_BASED = "./data/nyc_taxis.shuffled_full.parquet"
PATH_COLUMN_BASED: str = None

# column in a table containing the id of data items as in the original data

PROCESS_CHUNK_CALLBACK: Callable[[pd.DataFrame], pd.DataFrame] = None

DATA_DB = "data"  # name of view on the data under PATH
COLUMN_DATA_DB = "column_data"  # name of view on the data under PATH_COLUMN_BASED
PROCESSED_DB = "processed"  # name of database containing ids of processed data
LAST_UPDATE_DB = "last_updated"  # name of the
DOI_DB = "doi"  # name of database containing current doi values

ID = "tripID"  # column in a table containing the id of data items as in the original data
DOI = "doi"  # column in a table containing the doi value
CHUNK = "chunk"  # column in a table storing the chunk an item was processed
TIMESTAMP = "timestamp_"  # column in a table storing a timestamp for when a datum was updated
NOW = "current_timestamp"  # shorthand in duckdb for the current date and time

ID_INDEX = 0

cursor = duckdb.connect()  # database connection

DIMENSION_EXTENTS = {
  "VendorID": {"min": 1, "max": 2},
  "passenger_count": {"min": 0, "max": 192},
  "trip_distance": {"min": 0, "max": 50},
  "RatecodeID": {"min": 1, "max": 6},
  "PULocationID": {"min": 1, "max": 265},
  "DOLocationID": {"min": 1, "max": 265},
  "payment_type": {"min": 1, "max": 5},
  "fare_amount": {"min": -800, "max": 907070.24},
  "extra": {"min": -80, "max": 96.64},
  "mta_tax": {"min": -80, "max": 150},
  "tip_amount": {"min": 0, "max": 1000},
  "toll_amount": {"min": -52.5, "max": 1650},
  "improvement_surcharge": {"min": -0.3, "max": 4000.3},
  "total_amount": {"min": 0, "max": 300},
  # computed dimensions
  "trip_duration": {"min": 0, "max": 6000},
  "tip_ratio": {"min": 0, "max": 1}
}


def create_tables(row_data_path: str, column_data_path: str, id_column: str, total_size: int,
                  process_chunk_callback=None):
  global PATH, PATH_COLUMN_BASED, ID, TOTAL_SIZE, PROCESS_CHUNK_CALLBACK

  if None in [row_data_path, column_data_path, id_column, total_size]:
    raise Exception("missing parameter when initializing database")

  PATH = row_data_path
  PATH_COLUMN_BASED = column_data_path
  ID = id_column
  TOTAL_SIZE = total_size
  PROCESS_CHUNK_CALLBACK = process_chunk_callback  # if None, no processing is applied

  cursor.execute(f"CREATE VIEW {DATA_DB} "
                 f"AS SELECT * FROM read_csv_auto('{PATH}')")
  cursor.execute(f"CREATE VIEW {COLUMN_DATA_DB} "
                 f"AS SELECT * FROM parquet_scan('{PATH_COLUMN_BASED}')")
  cursor.execute(f"CREATE TABLE {PROCESSED_DB} "
                 f"({ID} VARCHAR UNIQUE PRIMARY KEY, {CHUNK} INTEGER)")
  cursor.execute(f"CREATE TABLE {DOI_DB} "
                 f"({ID} VARCHAR UNIQUE PRIMARY KEY,{DOI} VARCHAR)")
  cursor.execute(f"CREATE TABLE {LAST_UPDATE_DB} "
                 f"({ID} VARCHAR UNIQUE PRIMARY KEY, {TIMESTAMP} TIMESTAMP)")


def drop_tables():
  cursor.execute(f"DROP TABLE IF EXISTS {PROCESSED_DB}")
  cursor.execute(f"DROP TABLE IF EXISTS {LAST_UPDATE_DB}")
  cursor.execute(f"DROP TABLE IF EXISTS {DOI_DB}")
  cursor.execute(f"DROP VIEW IF EXISTS {DATA_DB}")
  cursor.execute(f"DROP VIEW IF EXISTS {COLUMN_DATA_DB}")


def reset_progression():
  cursor.execute(f"DELETE FROM {PROCESSED_DB}")
  cursor.execute(f"DELETE FROM {LAST_UPDATE_DB}")
  cursor.execute(f"DELETE FROM {DOI_DB}")


def mark_ids_processed(ids: List):
  if len(ids) == 0:
    return

  if len(ids) > 10000:
    # optimization: when too many ids get loaded, the query becomes too long. Therefore run this
    # operation recursively in two parts until the threshold is cleared
    mark_ids_processed(ids[:round(len(ids) / 2)])
    mark_ids_processed(ids[round(len(ids) / 2):])
    return

  chunk = cursor.execute(f"SELECT MAX({CHUNK}) FROM {PROCESSED_DB}").fetchall()[0]
  chunk = chunk[0] + 1 if chunk[0] is not None else 0
  chunked_values = "('" + f"',{chunk}),('".join(ids) + f"',{chunk})"
  timestamped_values = "('" + f"',{NOW}),('".join(ids) + f"',{NOW})"

  query = f"INSERT INTO {PROCESSED_DB} ({ID}, {CHUNK}) VALUES {chunked_values}"
  cursor.execute(query)
  query = f"INSERT INTO {LAST_UPDATE_DB} ({ID}, {TIMESTAMP}) VALUES {timestamped_values}"
  cursor.execute(query)


def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
  if len(chunk) == 0:
    return chunk
  elif PROCESS_CHUNK_CALLBACK is None:
    return chunk

  return PROCESS_CHUNK_CALLBACK(chunk)


def get_from_db(db_name: str, query_filters: List, dimensions: List, distinct=False,
                as_df=False):
  where_clause = ""
  for filter in query_filters:
    if len(where_clause) == 0:
      where_clause = f"{filter}"
    else:
      where_clause = f"{where_clause} AND {filter}"

  if len(where_clause) == 0:
    return np.empty(0) if as_df else []

  columns = dimensions if isinstance(dimensions, str) else ",".join(dimensions)

  select = "SELECT DISTINCT" if distinct else "SELECT"
  query = f"{select} {columns} FROM {db_name} WHERE {where_clause}"

  if as_df:
    return cursor.execute(query).fetchdf()
  else:
    return cursor.execute(query).fetchall()


def get_from_data(query_filters: List, dimensions="*", distinct=False, as_df=False):
  return get_from_db(DATA_DB, query_filters, dimensions, distinct, as_df)


def get_from_column_data(query_filters: List, dimensions="*", distinct=False, as_df=False):
  return get_from_db(COLUMN_DATA_DB, query_filters, dimensions, distinct, as_df)


def get_from_processed(query_filters: List, dimensions="*", distinct=False, as_df=False):
  return get_from_db(PROCESSED_DB, query_filters, dimensions, distinct, as_df)


def get_from_latest_update(query_filters: List, dimensions="*", distinct=False, as_df=False):
  return get_from_db(LAST_UPDATE_DB, query_filters, dimensions, distinct, as_df)


def get_from_doi(query_filters: List, dimensions="*", distinct=False, as_df=False):
  return get_from_db(DOI_DB, query_filters, dimensions, distinct, as_df)


def get_next_chunk_from_db(chunk_size: int, as_df=False):
  query = f"SELECT * \
            FROM {DATA_DB} \
            WHERE {ID} NOT IN (SELECT {ID} FROM {PROCESSED_DB}) \
            LIMIT {chunk_size}"

  next_chunk = cursor.execute(query).fetchdf()
  next_chunk = process_chunk(next_chunk)
  next_chunk[ID] = next_chunk[ID].astype(str)
  ids = next_chunk[ID].to_list()

  mark_ids_processed(ids)
  return next_chunk if as_df else next_chunk.values.tolist()


def update_last_update(ids: List):
  ids_list_str = list(map(str, ids))
  ids_str = f"{','.join(ids_list_str)}"

  query = f"UPDATE {LAST_UPDATE_DB} SET {TIMESTAMP}={NOW} WHERE {ID} IN ({ids_str})"
  cursor.execute(query)


def save_dois(ids: List, dois: List):
  if len(ids) == 0:
    return

  if len(ids) > 10000:
    # optimization: when too many ids get loaded, the query becomes too long. Therefore run this
    # operation recursively in two parts until the threshold is cleared
    split = round(len(ids) / 2)
    save_dois(ids[:split], dois[:split])
    save_dois(ids[split:], dois[split:])
    return

  values = ""
  for i, id in enumerate(ids):
    values = f"{values}({id},{dois[i]})"
    if i < len(ids) - 1:
      values += ","
  query = f"INSERT INTO {DOI_DB} ({ID}, {DOI}) VALUES {values}"
  cursor.execute(query)
  update_last_update(ids)


def get_dois(ids: List):
  if len(ids) == 0:
    return np.empty(0)
  if len(ids) == 1:
    ids += ids
  query = f"SELECT {DOI} FROM {DOI_DB} WHERE {ID} IN {tuple(ids)}"
  return cursor.execute(query).fetchnumpy()[DOI.lower()]


def update_dois(ids: List, dois: List):
  # code below contains the slow approach using upate, which is slowing down the computation
  # noticably (see delete -> insert alternative below)
  def update_doi(id: str, doi: str):
    query = f"UPDATE {DOI_DB} SET {DOI}={doi} WHERE {ID}={id}"
    cursor.execute(query)

  if len(ids) == 0:
    return

  for i, id in enumerate(ids):
    update_doi(str(id), dois[i])

  # we suspect the code below is faster than individual updates, but because of a bug in duckdb
  # that leads to primary key inconsistencies when doing insert(a)->delete(a)->insert(a), we fall
  # back to the slower version
  # ids_list = map(str, ids)
  # ids_list = ",".join(ids_list)
  # query = f"DELETE FROM {DOI_DB} WHERE {ID} IN ({ids_list})"
  # cursor.execute(query)

  # save_dois(ids, dois)

  update_last_update(ids)


def get_dimensions_in_data():
  query = f"SELECT * FROM {DATA_DB} LIMIT 1"
  item = cursor.execute(query).fetchdf()
  dimensions = list(item.columns)
  dimensions = dimensions + ["trip_duration", "tip_ratio"]
  return dimensions


def get_data_size():
  # computing count() on-demand takes too long for large data
  # query = f"SELECT COUNT(*) FROM {TABLE}"
  # size = cursor.execute(query).fetchall()[0]
  return TOTAL_SIZE


def get_random_sample(chunk_size: int):
  dimensions = 5
  return [[random.random() for __ in range(dimensions)] for _ in range(chunk_size)]


def get_random_dims(dimensions: int):
  return [f"dimension_{str(i)}" for i in range(dimensions)]


def get_dimension_extent(dimension: str):
  return DIMENSION_EXTENTS.get(dimension)


def get_items_for_ids(ids: List, as_df=False):
  if len(ids) == 1:
    ids += ids
  return get_from_column_data([f"{ID} IN {tuple(ids)}"], as_df=as_df)
