import pandas as pd

if __name__ == "__main__":
  import sys
  if len(sys.argv) == 1:
    raise Exception("Please provide a path to a csv file as parameter")

  path = sys.argv[1]
  df = pd.read_csv(path)

  if len(sys.argv) == 2:
    print(df.to_csv(), index_label="tripID")
  else:
    df.to_csv(sys.argv[2], index_label="tripID")
