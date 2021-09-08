import duckdb
import random

TOTAL_SIZE = 112145904

# database constants
PATH = "./data/nyc_taxis.shuffled_full.csv.gz"
TABLE = "data"
PROCESSED = "processed" # name of database containing ids of processed data
SELECTED = "selected"
PROVENANCE = "provenance"
DOI = "doi"
ID = "tripID"
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
  "total_amount": {"min": 0, "max": 300 }
}


def initialize_db():
  cursor.execute(f"CREATE VIEW {TABLE} AS SELECT * FROM read_csv_auto('{PATH}')")
  cursor.execute(f"CREATE TABLE {PROCESSED} ({ID} VARCHAR UNIQUE PRIMARY KEY)")
  cursor.execute(f"CREATE TABLE {SELECTED} ({ID} VARCHAR UNIQUE PRIMARY KEY)")
  cursor.execute(f"CREATE TABLE {PROVENANCE} ({ID} VARCHAR UNIQUE PRIMARY KEY,{DOI} DOUBLE)")


def mark_ids_plotted(ids: list):
  values = "('"+"'),('".join(ids)+"')"
  query = f"INSERT INTO {PROCESSED} ({ID}) VALUES {values}"
  cursor.execute(query)


def mark_ids_selected(ids: list[str]):
  if len(ids) == 0:
    return
  query = f"DELETE FROM {SELECTED}"
  cursor.execute(query)
  values = "('"+"'),('".join(ids)+"')"
  query = f"INSERT INTO {SELECTED} ({ID}) VALUES {values}"
  cursor.execute(query)


def mark_ids_provenance(ids: list[str], doi_values: list[float]):
  if len(ids) == 0:
    return
  query = f"DELETE FROM {PROVENANCE}"
  cursor.execute(query)
  values = ""
  for index, id in enumerate(ids):
    if index == 0:
      values = f"({id},{doi_values[index]})"
    else:
      values = f"({id},{doi_values[index]}),{values}"
  query = f"INSERT INTO {PROVENANCE} ({ID},{DOI}) VALUES {values}"
  cursor.execute(query)


def is_id_selected(id: str):
  query = f"SELECT * FROM {SELECTED} WHERE {ID}={id}"
  result = cursor.execute(query).fetchall()
  return len(result) > 0


def get_id_from_provenance(id: str):
  query = f"SELECT * FROM {PROVENANCE} WHERE {ID}={id}"
  result = cursor.execute(query).fetchall()
  if len(result) > 0:
    return result[0]
  else:
    return result


def is_id_in_provenance(id: str):
  result = get_id_from_provenance(id)
  return len(result) > 0


def get_next_chunk_from_db(chunk_size: int):
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


def get_random_sample(chunk_size: int):
  dimensions = 5
  return [ [random.random() for __ in range(dimensions)] for _ in range(chunk_size) ];


def get_random_dims(dimensions: int):
  return [f"dimension_{str(i)}" for i in range(dimensions)]


def get_dimension_extent(dimension: str):
  return DIMENSION_EXTENTS.get(dimension)


def get_items_for_ids(ids: list[str]):
  id_list = "'"+"','".join(ids)+"'"
  query = f"SELECT * FROM {TABLE} WHERE {ID} IN ({id_list})"
  df = cursor.execute(query).fetchdf()
  items = df.to_numpy()
  return items


def reset_progression():
  query = f"DELETE FROM {PROCESSED}"
  cursor.execute(query)