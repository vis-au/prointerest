# Downloading Datasets

This document describes how to obtain the different datasets used by ProInterest.

## 2018 NYC Taxi Dataset

1. Download the dataset from the [websites of the City of New York](https://data.cityofnewyork.us/Traasportation/2018-Yellow-Taxi-Trip-Data/t29m-gskq) as a CSV file.
2. Using a tool like [7zip](https://www.7-zip.org/), compress the CSV file to gzip and rename it to `nyc_taxis.shuffled_full.csv.gz"`.
3. Place the file in this (`server/data/`) directory.
4. Generate the index column by running the `add_id_column_to_csv.py` script.
5. (Only necessary if when using the graphical interface) Generate a PARQUET version of the dataset, for example using [this script](https://github.com/vis-au/progressive-steering/blob/master/data/csv_to_parquet.py).
