from flask import Flask, jsonify
import duckdb
import random

app = Flask(__name__)

CHUNK_SIZE = 100
DIMENSIONS = 5

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


def get_next_chunk_from_db():
  query = f"SELECT * FROM {TABLE} WHERE {ID} NOT IN (SELECT {ID} FROM {PROCESSED}) LIMIT {CHUNK_SIZE}"
  next_chunk = cursor.execute(query).fetchall()
  ids = [str(item[ID_INDEX]) for item in next_chunk]
  mark_ids_plotted(ids)

  return next_chunk


def get_dimensions_in_data():
  query = f"SELECT * FROM {TABLE} LIMIT 1"
  item = cursor.execute(query).fetchdf()
  dimensions = list(item.columns)
  return dimensions


def get_random_sample():
  return [ [random.random() for __ in range(DIMENSIONS)] for _ in range(CHUNK_SIZE) ];


def get_random_dims():
  return [f"dimension_{str(i)}" for i in range(DIMENSIONS)]



def cors_response(payload):
  response = jsonify(payload)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


@app.route("/")
def hello_world():
  return "Ok. Flask server successfully launched."


@app.route("/dimensions", methods=["GET"])
def get_dimensions():
  dims = get_dimensions_in_data()
  return cors_response(dims)


@app.route("/next_chunk", methods=["GET"])
def get_next_chunk():
  # chunk = get_random_sample()
  chunk = get_next_chunk_from_db()
  return cors_response(chunk)


if __name__ == "__main__":
  initialize_db()
  app.run(debug=True)