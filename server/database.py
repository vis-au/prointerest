import duckdb
import random

TOTAL_SIZE = 112145904

# database constants
PATH = "./data/nyc_taxis.shuffled_full.csv.gz"
TABLE = "data"
PROCESSED = "processed" # name of database containing ids of processed data
ID = "tripID"
ID_INDEX = 0

cursor = duckdb.connect() # database connection


def initialize_db():
  cursor.execute(f"CREATE VIEW {TABLE} AS SELECT * FROM read_csv_auto('{PATH}')")
  cursor.execute(f"CREATE TABLE {PROCESSED} ({ID} VARCHAR UNIQUE PRIMARY KEY)")


def mark_ids_plotted(ids: list):
  values = "('"+"'),('".join(ids)+"')"
  query = f"INSERT INTO {PROCESSED} ({ID}) VALUES {values}"
  cursor.execute(query)


def get_next_chunk_from_db(chunk_size):
  query = f"SELECT * FROM {TABLE} WHERE {ID} NOT IN (SELECT {ID} FROM {PROCESSED}) LIMIT {chunk_size}"
  next_chunk = cursor.execute(query).fetchall()
  ids = [str(item[ID_INDEX]) for item in next_chunk]
  mark_ids_plotted(ids)

  return next_chunk


def get_dimensions_in_data():
  query = f"SELECT * FROM {TABLE} LIMIT 1"
  item = cursor.execute(query).fetchdf()
  dimensions = list(item.columns)
  return dimensions

def get_data_size():
  # computing count() on-demand takes too long for large data
  # query = f"SELECT COUNT(*) FROM {TABLE}"
  # size = cursor.execute(query).fetchall()[0]
  return TOTAL_SIZE


def get_random_sample(chunk_size):
  dimensions = 5
  return [ [random.random() for __ in range(dimensions)] for _ in range(chunk_size) ];


def get_random_dims(dimensions):
  return [f"dimension_{str(i)}" for i in range(dimensions)]


def get_items_for_ids(ids: list[str]):
  id_list = "'"+"','".join(ids)+"'"
  query = f"SELECT * FROM {TABLE} WHERE {ID} IN ({id_list})"
  df = cursor.execute(query).fetchdf()
  items = df.to_numpy()
  return items

def reset_progression():
  query = f"DELETE FROM {PROCESSED}"
  cursor.execute(query)