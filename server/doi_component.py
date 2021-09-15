import numpy as np
from pandas.core.frame import DataFrame
from sklearn.tree import DecisionTreeRegressor

class DoiComponent:
  '''
  Describes a general component of a progressive degree-of-interest function. It can either be prior
  or posterior component. Prior components derive the degree-of-interest for each data item in the
  context of other data without considering user behavior. Posterior components on the other hand
  derive the degree-of-interest for each data item by also considering user interactions, for
  example by measuring the similarity to a focus point set by the user or by.
  '''
  def __init__(self) -> None:
    self.weights: dict[str, float] = {}
    self.current_interest = np.empty(shape=(0, 2))
    self.predictor: DecisionTreeRegressor = DecisionTreeRegressor(random_state=0)


  def set_components(self, weights: dict[str, float]):
    '''
    Specify components of the doi function, such as weights. Expects a dictionary that for each
    component specifies a numeric value.
    '''
    self.weights = weights


  def update(self, data):
    '''
    Send more information to the doi function based on the progression. This could for instance be
    a set of adjusted function parameters.
    '''
    pass


  def compute_doi(self, X: DataFrame):
    '''
    Compute the degree of interest over a matrix of shape (n, m) using the degree-of-interest
    function of this object. Outputs a vector y of shape (n, 1), containing the actual doi for
    each item.
    '''
    pass


  def predict_doi(self, X: DataFrame):
    '''
    Given the state of the doi predictor, predicts the degree of interest for the given a matrix X
    with shape (n, m) without evaluating the full function. Returns a vector y of shape (n, 1),
    containing the predicted doi for each item.
    '''
    pass


  def get_prediction_error(self, X: DataFrame):
    '''
    A benchmarking function for the predictor: How accurate are the predictions based on the current
    model? Takes a matrix X with shape (n, m) as input, then computes both the prediction and the
    actual doi for this matrix, therefore has high runtime. Outputs the place-wise error as a vector
    of shape (n, 1).
    '''
    pass

  def train(self):
    pass
