from typing import Any
from flask import Flask, json, jsonify, request

from database import *
from doi_function import *
from scagnostics_component import SCATTERPLOT_AXES

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


@app.route("/extent/<dimension>", methods=["GET"])
def get_dim_extent(dimension):
  extent = get_dimension_extent(dimension)
  return cors_response(extent)


@app.route("/next_chunk", methods=["GET"])
def get_next_chunk():
  chunk_size = int(request.args.get("size"))
  chunk = get_next_chunk_from_db(chunk_size)

  ids = np.array(chunk)[:, 0].tolist()
  doi = compute_dois(chunk).tolist()
  bins, labels = compute_doi_classes(doi)
  save_dois(ids, doi, labels)

  return cors_response({
    "chunk": chunk,
    "doi": doi,
    "labels": labels,
    "bins": bins
  })


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

  if component == "components":
    set_component_weights(weights)
  elif component == "prior":
    set_prior_weights(weights)
  elif component == "posterior":
    set_posterior_weights(weights)
  elif component == "scagnostics":
    set_scagnostic_weights(weights)
  elif component == "provenance":
    set_provenance_weights(weights)

  return cors_response("ok")


@app.route("/dimensions", methods=["POST"])
def send_interesting_dimensions():
  dimensions = json.loads(request.data)["dimensions"]
  set_dimensions_of_interest(dimensions)
  return cors_response(True)


@app.route("/dimension_range", methods=["POST"])
def send_interesting_range():
  res = json.loads(request.data)
  dimension = res["dimension"]
  min_value = res["min"]
  max_value = res["max"]
  set_dimension_range_of_interest(dimension, min_value, max_value)

  return cors_response(True)


@app.route("/axis", methods=["GET"])
def send_axis_dimension():
  axis = request.args.get("axis")
  dimension = request.args.get("dimension")

  if axis not in ["x", "y"]:
    return cors_response(False)

  SCATTERPLOT_AXES[axis] = dimension
  return cors_response(True)


@app.route("/config/<component>", methods=["POST"])
def send_configuration(component):
  if component == "outlierness":
    if request.args.get("metric") is not None:
      metric = request.args.get("metric")
      set_outlierness_metric(metric)
  elif component == "provenance":
    if request.args.get("weights") is not None:
      weights = request.args.get("weights")
      print(weights)
    if request.args.get("threshold") is not None:
      threshold = request.args.get("threshold")
      print(threshold)
    if request.args.get("log_size") is not None:
      log_size = request.args.get("log_size")
      print(log_size)

  return cors_response(True)


@app.route("/interaction", methods=["POST"])
def send_interaction():
  res = json.loads(request.data)
  ids = res["ids"]
  mode = res["mode"] # "brush", "zoom", "selection"

  log_interaction(mode, ids)

  return cors_response(True)


@app.route("/suggested_items", methods=["GET"])
def get_suggested_items():
  pass


# @app.route("/doi", methods=["POST"])
# def get_doi():
#   items: list[list[Any]] = json.loads(request.data)["items"]

#   interest = compute_dois(items)
#   return cors_response(interest)


@app.route("/prediction", methods=["GET"])
def get_prediction():
  items: list[list[Any]] = json.loads(request.data)["items"]
  return cors_response([])


if __name__ == "__main__":
  initialize_db()
  app.run(debug=True)