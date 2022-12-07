import json
from flask import Flask, json, jsonify, request

from database import *
from doi_function import *
from steering import *

app = Flask(__name__)

STEERING_FILTERS: str or dict = (
    {}
)  # HACK to allow for both sherpa-like and sbe-like steering


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
    chunk = get_next_chunk_from_db(chunk_size, filters=STEERING_FILTERS)

    ids = np.array(chunk)[:, 0].tolist()
    dois, updated_ids, updated_dois = compute_dois(chunk)
    save_dois(ids, dois.tolist())

    return cors_response(
        {
            "chunk": chunk,
            "dois": dois.tolist(),
            "updated_ids": updated_ids,
            "updated_dois": updated_dois.tolist(),
        }
    )


@app.route("/size", methods=["GET"])
def get_size():
    size = get_data_size()
    return cors_response(size)


@app.route("/reset", methods=["GET"])
def reset():
    global STEERING_FILTERS
    STEERING_FILTERS = {}
    reset_progression()
    reset_doi_component()
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
    elif component == "outlierness":
        set_outlierness_weights(weights)
    elif component == "dimensions":
        set_dimension_weights(weights)

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


def set_steering_filters(filters: str or dict):
    global STEERING_FILTERS
    STEERING_FILTERS = filters


@app.route("/steer", methods=["POST"])
def send_steering_filters():
    res = json.loads(request.data)
    filters = res[
        "filters"
    ]  # dict containing min/max filters (val) for dimensions in the data (key)
    set_steering_filters(filters)

    return cors_response(True)


@app.route("/train_tree", methods=["POST"])
def get_train_decision_tree():
    res = json.loads(request.data)

    # make dataframe with items that are of interest to the user
    items = res["items"]
    dimensions = res["dimensions"]
    items_df = pd.DataFrame(np.array(items), columns=dimensions)

    # FIXME: use the actual subspace of interest!
    items_df = items_df[
        [
            "trip_distance",
            "total_amount",
            "tip_amount",
            "trip_duration",
            "passenger_count",
            "fare_amount",
        ]
    ]

    # a vector indicating either whether an item is marked as interesting in the frontend (for
    # classification) or its current inteterest as numeric value (for regression)
    label = res["label"]
    label = np.array(label)

    # which task to perform on the data, i.e., whether to use a regression/classification tree
    use_regression = res["use_regression"]

    # get the tree model
    tree_dict = get_decision_tree(items_df, label, use_regression=use_regression)

    return cors_response(tree_dict)


@app.route("/steer-by-example", methods=["POST"])
def send_steering_by_examples():
    res = json.loads(request.data)

    # list of items that are of interest to the user
    items = res["items"]
    columns = res["dimensions"]
    items = pd.DataFrame(np.array(items), columns=columns)

    # FIXME: use the actual subspace of interest!
    items = items[["trip_distance", "total_amount", "tip_amount", "trip_duration"]]

    # vector indicating whether an item is marked as interesting in the frontend
    is_interesting = res["isInteresting"]
    is_interesting = np.array(is_interesting)

    # The decision tree is trained on all dimensions in the items
    filters = get_steering_condition(items, is_interesting, "sql")

    set_steering_filters(filters)

    return cors_response(True)


@app.route("/axis", methods=["GET"])
def send_axis_dimension():
    axis = request.args.get("axis")
    dimension = request.args.get("dimension")

    if axis not in ["x", "y"]:
        return cors_response(False)

    set_scatterplot_axis(axis, dimension)
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
    mode = res["mode"]  # "brush", "zoom", "selection"

    log_interaction(mode, ids)

    return cors_response(True)


@app.route("/suggested_items", methods=["GET"])
def get_suggested_items():
    pass


@app.route("/doi/<ids>", methods=["POST"])
def get_doi(ids):
    interest = get_dois(ids)
    return cors_response(interest)


@app.route("/prediction", methods=["GET"])
def get_prediction():
    items: list
    return cors_response([])


data_path = "./data/nyc_taxis.shuffled_full.csv.gz"
column_data_path = "./data/nyc_taxis.shuffled_full.parquet"
id_column = "tripID"
total_db_size = 112145904  # full size of database
n_dims = 17  # number of dimensions in the data


def taxi_process_chunk(chunk: pd.DataFrame):
    dropoff = chunk["tpep_dropoff_datetime"]
    pickup = chunk["tpep_pickup_datetime"]
    chunk["duration"] = dropoff - pickup
    chunk["duration"] = chunk["duration"].apply(lambda x: x.total_seconds())
    chunk["ratio"] = chunk["tip_amount"] / chunk["total_amount"]
    return chunk


if __name__ == "__main__":
    drop_tables()
    create_tables(
        row_data_path=data_path,
        column_data_path=column_data_path,
        id_column=id_column,
        total_size=total_db_size,
        process_chunk_callback=taxi_process_chunk,
    )
    app.run(debug=True)
