import duckdb
import numpy as np
import random

TOTAL_SIZE = 112145904

# database constants
PATH = "./data/nyc_taxis.shuffled_full.csv.gz" # path to the (compressed) csv file

CSV_DB = "data" # name of view on the csv file
PROCESSED_DB = "processed" # name of database containing ids of processed data
LAST_UPDATE_DB = "last_updated" # name of the
DOI_DB = "doi" # name of database containing current doi values

ID = "tripID" # column in a table containing the id of data items as in the original data
DOI = "doi" # column in a table containing the doi value
BIN = "label" # column in a table containing the current label assigned to a doi
CHUNK = "chunk" # column in a table storing the chunk an item was processed

ID_INDEX = 0

cursor = duckdb.connect() # database connection

DIMENSION_EXTENTS = {
  "VendorID": {"min": 1, "max": 2 },
  "passenger_count": {"min": 0, "max": 192 },
  "trip_distance": {"min": 0, "max": 50 },
  "RatecodeID": {"min": 1, "max": 6 },
  "PULocationID": {"min": 1, "max": 265 },
  "DOLocationID": {"min": 1, "max": 265 },
  "payment_type": {"min": 1, "max": 5 },
  "fare_amount": {"min": -800, "max": 907070.24 },
  "extra": {"min": -80, "max": 96.64 },
  "mta_tax": {"min": -80, "max": 150 },
  "tip_amount": {"min": 0, "max": 1000 },
  "toll_amount": {"min": -52.5, "max": 1650 },
  "improvement_surcharge": {"min": -0.3, "max": 4000.3 },
  "total_amount": {"min": 0, "max": 300 },
  # computed dimensions
  "trip_duration": {"min": 0, "max": 6000},
  "tip_ratio": {"min": 0, "max": 1}
}


def initialize_db(path=None):
  global PATH
  if path is not None and len(path) > 0:
    PATH = path
  cursor.execute(f"CREATE VIEW {CSV_DB} AS SELECT * FROM read_csv_auto('{PATH}')")
  cursor.execute(f"CREATE TABLE {PROCESSED_DB} ({ID} VARCHAR UNIQUE PRIMARY KEY, {CHUNK} INTEGER)")
  cursor.execute(f"CREATE TABLE {DOI_DB} ({ID} VARCHAR UNIQUE PRIMARY KEY,{DOI} VARCHAR, {BIN} VARCHAR)")
  cursor.execute(f"CREATE TABLE {LAST_UPDATE_DB} ({ID} VARCHAR UNIQUE PRIMARY KEY, {CHUNK} INTEGER)")


def mark_ids_plotted(ids: list):
  chunk = cursor.execute(f"SELECT MAX({CHUNK}) FROM {PROCESSED_DB}").fetchall()[0]
  chunk = chunk[0] + 1 if chunk[0] is not None else 0
  values = "('"+f"',{chunk}),('".join(ids)+f"',{chunk})"

  query = f"INSERT INTO {PROCESSED_DB} ({ID}, {CHUNK}) VALUES {values}"
  cursor.execute(query)
  query = f"INSERT INTO {LAST_UPDATE_DB} ({ID}, {CHUNK}) VALUES {values}"
  cursor.execute(query)

def process_chunk(chunk: list[tuple[float]]):
  extended_chunk = []
  for tuple in chunk:
    pickup_datetime = tuple[2]
    dropoff_datetime = tuple[3]
    duration = (dropoff_datetime-pickup_datetime).total_seconds()
    tuple = tuple + (duration, )
    ratio = tuple[15] / tuple[17]
    tuple = tuple + (ratio, )
    extended_chunk.append(tuple)
  return extended_chunk


def update_dois(ids: list[str], values: list[str], chunk: int):
  for i, id in enumerate(ids):
    cursor.execute(f"UPDATE {PROCESSED_DB} SET {DOI}={values[i]} WHERE {ID}={id}")
    cursor.execute(f"UPDATE {LAST_UPDATE_DB} SET {CHUNK}={chunk} WHERE {ID}={id}")


def get_from_db(db_name: str, query_filters: list[str], dimensions: list[str], distinct=False, as_df=False):
  where_clause = ""
  for filter in query_filters:
    if len(where_clause) == 0:
      where_clause = f"{filter}"
    else:
      where_clause = f"{where_clause} AND {filter}"

  if len(where_clause) == 0:
    return np.empty(0) if as_df else []

  select = "SELECT DISTINCT" if distinct else "SELECT"
  query = f"{select} {dimensions} FROM {db_name} WHERE {where_clause}"

  if as_df:
    return cursor.execute(query).fetchdf()
  else:
    return cursor.execute(query).fetchall()


def get_from_data(query_filters: list[str], dimensions="*", distinct=False, as_df=False):
  return get_from_db(CSV_DB, query_filters, dimensions, distinct, as_df)


def get_from_processed(query_filters: list[str], dimensions="*", distinct=False, as_df=False):
  return get_from_db(PROCESSED_DB, query_filters, dimensions, distinct, as_df)


def get_from_latest_update(query_filters: list[str], dimensions="*", distinct=False, as_df=False):
  return get_from_db(LAST_UPDATE_DB, query_filters, dimensions, distinct, as_df)


def get_next_chunk_from_db(chunk_size: int):
  query = f"SELECT * FROM {CSV_DB} WHERE {ID} NOT IN (SELECT {ID} FROM {PROCESSED_DB}) LIMIT {chunk_size}"
  next_chunk = cursor.execute(query).fetchall()
  next_chunk = process_chunk(next_chunk)
  ids = [str(item[ID_INDEX]) for item in next_chunk]
  mark_ids_plotted(ids)
  return next_chunk


def save_dois(ids: list, dois: list, bins: list):
  values = ""
  for i, id in enumerate(ids):
    values = f"{values}({id},{dois[i]},{bins[i]})"
    if i < len(ids) - 1:
      values += ","
  query = f"INSERT INTO {DOI_DB} ({ID}, {DOI}, {BIN}) VALUES {values}"
  cursor.execute(query)


def get_dois(ids: list):
  id_list = ""
  for id in ids:
    id_list += str(id)
    if id != ids[-1]:
      id_list += ","
  query = f"SELECT {DOI} FROM {DOI_DB} WHERE {ID} IN ({id_list})"
  return cursor.execute(query).fetchnumpy()


def update_doi(id: str, doi: str):
  query = f"UPDATE {DOI_DB} SET {DOI}={doi} WHERE {ID}={id}"
  cursor.execute(query)


def update_dois(ids: list, dois: list):
  for i, id in enumerate(ids):
    update_doi(id, dois[i])


def get_dimensions_in_data():
  query = f"SELECT * FROM {CSV_DB} LIMIT 1"
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
  return [ [random.random() for __ in range(dimensions)] for _ in range(chunk_size) ];


def get_random_dims(dimensions: int):
  return [f"dimension_{str(i)}" for i in range(dimensions)]


def get_dimension_extent(dimension: str):
  return DIMENSION_EXTENTS.get(dimension)


def get_items_for_ids(ids: list[str]):
  id_list = "'"+"','".join(ids)+"'"
  query = f"SELECT * FROM {CSV_DB} WHERE {ID} IN ({id_list})"
  df = cursor.execute(query).fetchdf()
  items = df.to_numpy()
  return items


def drop_tables():
  cursor.execute(f"DROP TABLE IF EXISTS {PROCESSED_DB}")
  cursor.execute(f"DROP TABLE IF EXISTS {LAST_UPDATE_DB}")
  cursor.execute(f"DROP TABLE IF EXISTS {DOI_DB}")
  cursor.execute(f"DROP VIEW IF EXISTS {CSV_DB}")


def reset_progression():
  cursor.execute(f"DELETE FROM {PROCESSED_DB}")
  cursor.execute(f"DELETE FROM {LAST_UPDATE_DB}")
  cursor.execute(f"DELETE FROM {DOI_DB}")