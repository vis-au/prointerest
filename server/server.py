import numpy as np
from flask import Flask, json, jsonify, request

from database import get_data_size, get_dimensions_in_data, get_next_chunk_from_db, initialize_db, get_items_for_ids, reset_progression
from recommender import train

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
  return cors_response("ok")


@app.route("/interesting_ids", methods=["POST"])
def send_interesting_items():
  res = json.loads(request.data)
  ids = res["ids"]
  doi = res["doi"]

  # get numpy array for ids
  items = get_items_for_ids(ids)
  interest = np.array(doi)

  # send ids to predictor model
  train(items, interest)
  print("ooph")

  return cors_response(True)


@app.route("/get_prediction", methods=["POST"])
def get_prediction():
  print("predicting very hard ...")
  return cors_response([])


if __name__ == "__main__":
  initialize_db()
  app.run(debug=True)