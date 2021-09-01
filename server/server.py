from flask import Flask, abort, jsonify, request
import random

app = Flask(__name__)

CHUNK_SIZE = 100
DIMENSIONS = 5


def cors_response(payload):
  response = jsonify(payload)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


def get_random_sample():
  return [ [random.random() for __ in range(DIMENSIONS)] for _ in range(CHUNK_SIZE) ];


def get_random_dims():
  return [f"dimension_{str(i)}" for i in range(DIMENSIONS)]



@app.route("/")
def hello_world():
  return "Ok. Flask server successfully launched."


@app.route("/dimensions", methods=["GET"])
def get_dimensions():
  return cors_response(get_random_dims())


@app.route("/next_chunk", methods=["GET"])
def get_next_chunk():
  return cors_response(get_random_sample())


# @app.route("/create_pipeline/<id>", methods=["GET"])
# def create_pipeline(id):
#   PIPELINES[str(id)] = Pipeline(get_pipeline_config(request))
#   return cors_response("ok")


if __name__ == "__main__":
  app.run(debug=True)