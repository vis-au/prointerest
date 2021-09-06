from sklearn.svm import LinearSVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression

pipeline = make_pipeline(StandardScaler(), LinearSVR(random_state=0, tol=1e-5))

X, y = make_regression(n_features=4, random_state=0)
regr: LinearSVR = None # regression model


def train(X, y):
  global regr
  regr = pipeline.fit(X, y)


def predict(X):
  y = regr.predict(X)
  return y