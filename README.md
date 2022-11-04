# ProInterest
_Supporting progressive visualization with degree-of-interest functions._

## Prerequisites
* requires [nodeJS](https://nodejs.org/en/blog/release/v16.0.0/) version 16 or later, with [npm](https://www.npmjs.com/) version 7 or later
* requires [python 3.8](https://www.python.org/downloads/release/python-380/) (**NOTE:** due to a dependency on the [`pyscagnostics`](https://pypi.org/project/pyscagnostics/) package, later versions than 3.8 are currently NOT supported), with [pip]() version 22.

## Getting Started
To install ProInterest, you need to install both the frontend and backend components, located in their own subdirectories in this repository.


### Installing the Frontend
To install the frontend component, open a terminal in the `client/` directory and download the dependencies via npm:
```
npm install
```

### Installing the Backend
To install the backend component, open a terminal in the `server/` directory and download the dependencies via pip:
```
python -m pip install -r requirements.txt
```

### Downloading the Data
ProInterest uses the NYC taxi dataset, which can be downloaded from [NYC OpenData](https://data.cityofnewyork.us/Transportation/2018-Yellow-Taxi-Trip-Data/t29m-gskq). After downloading, place the data in the `server/data/` directory, with the file name `nyc_taxis.unshuffled_full.csv.gz`. Generate a `.parquet` file by running the `csv_to_parquet.py` script in the same directory, passing the `csv.gz` file as a parameter.


## Getting Started
With both frontend and backend installed, you can now launch ProInterest in your browser:

First, launch the server from your terminal inside the `server/` directory via
```
python server.py
```
and afterwards launch the frontend via
```
npm run dev
```
After a few seconds, you can navigate your browser to [https://localhost:3000](https://localhost:3000).


## Running the Benchmarks
The benchmarks we report on in our paper are located in the [server/benchmarks/](./server/benchmarks/) directory.
The `test_cases.json` file defines presets you can use to replicate our results, by running
```
python benchmarks.py <index in test_cases.json> composite
```
Afterwards, you can visualize the results inside the [`analysis.ipynb`](./server/benchmarks/analysis.ipynb) notebook.