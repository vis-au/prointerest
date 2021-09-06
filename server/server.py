from typing import Any
from flask import Flask, json, jsonify, request

from database import *
from doi_function import *
from recommender import *

app = Flask(__name__)



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
  chunk_size = int(request.args.get("size"))
  # chunk = get_random_sample(chunk_size)
  chunk = get_next_chunk_from_db(chunk_size)
  return cors_response(chunk)


@app.route("/size", methods=["GET"])
def get_size():
  size = get_data_size()
  return cors_response(size)


@app.route("/reset", methods=["GET"])
def reset():
  reset_progression()
  return cors_response(True)


@app.route("/weights/<component>", methods=["POST"])
def send_weights(component: str):
  weights = json.loads(request.data)["weights"]

  if component == "prior":
    set_prior_weights(weights)
  elif component == "posterior":
    set_posterior_weights(weights)
  elif component == "scagnostics":
    set_scagnostic_weights(weights)

  return cors_response("ok")


@app.route("/dimensions", methods=["POST"])
def send_interesting_dimensions():
  dimensions = json.loads(request.data)["dimensions"]
  set_dimensions_of_interest(dimensions)
  return cors_response(True)


@app.route("/outlierness_metric/<metric>", methods=["POST"])
def send_outlierness_metric(metric: str):
  set_outlierness_metric(metric)
  return cors_response(True)


@app.route("/selected_items", methods=["POST"])
def send_selected_items():
  # list of list of values, where the first entry is the item id
  items: list[list[Any]] = json.loads(request.data)["items"]

  # ids is a list of strings
  ids: list[str] = [str(item[0]) for item in items]

  set_selected_item_ids(ids)
  return cors_response(True)


@app.route("/interesting_items", methods=["POST"])
def send_interesting_items():
  res = json.loads(request.data)
  ids = res["ids"]
  doi = res["doi"]

  set_provenance_items(ids, doi)

  return cors_response(True)


@app.route("/suggested_items", methods=["GET"])
def get_suggested_items():
  pass


@app.route("/doi", methods=["POST"])
def get_doi():
  items: list[list[Any]] = json.loads(request.data)["items"]

  interest = compute_dois(items)
  return cors_response(interest)


@app.route("/prediction", methods=["GET"])
def get_prediction():
  items: list[list[Any]] = json.loads(request.data)["items"]
  return cors_response([])


if __name__ == "__main__":
  initialize_db()
  app.run(debug=True)