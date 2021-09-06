import numpy as np
from sklearn.svm import LinearSVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression

from doi_function import get_interest


pipeline = make_pipeline(StandardScaler(), LinearSVR(random_state=0, tol=1e-5))

X, y = make_regression(n_features=4, random_state=0)
regr: LinearSVR = None # regression model


def train(X, y):
  global regr
  y = np.array([get_interest(X[i]) for i in X])
  regr = pipeline.fit(X, y)


def predict(X):
  y = regr.predict(X)
  return y