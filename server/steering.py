# steering-by-example module, reproduced from
# https://github.com/vis-au/progressive-steering/blob/master/backend/steering_duckdb.py
import json
import numpy as np
import pandas as pd
from sklearn.tree import (
    DecisionTreeClassifier,
    DecisionTreeRegressor,
    _tree,
    BaseDecisionTree,
)

# global variables used for generating the steering condition
feature = None
threshold = None


def _find_path(tree, node_numb, path, x):
    path.append(node_numb)

    children_left = tree.children_left
    children_right = tree.children_right

    if node_numb == x:
        return True

    left = False
    right = False

    if children_left[node_numb] != -1:
        left = _find_path(tree, children_left[node_numb], path, x)
    if children_right[node_numb] != -1:
        right = _find_path(tree, children_right[node_numb], path, x)
    if left or right:
        return True

    path.remove(node_numb)

    return False


def _extract_paths(X, model):
    tree = model.tree_
    paths = {}
    leave_id = model.apply(X)
    for leaf in np.unique(leave_id):
        if model.classes_[np.argmax(model.tree_.value[leaf])] == 1:
            path_leaf = []
            _find_path(tree, 0, path_leaf, leaf)
            paths[leaf] = np.unique(np.sort(path_leaf))

    return paths


def _get_rule(tree, path, column_names):
    children_left = tree.children_left

    mask = ""
    for index, node in enumerate(path):
        # We check if we are not in the leaf
        if index != len(path) - 1:
            # Do we go under or over the threshold ?
            if children_left[node] == path[index + 1]:
                mask += "(df['{}']<= {}) \t ".format(
                    column_names[feature[node]], threshold[node]
                )
            else:
                mask += "(df['{}']> {}) \t ".format(
                    column_names[feature[node]], threshold[node]
                )
    # We insert the & at the right places
    mask = mask.replace("\t", "&", mask.count("\t") - 1)
    mask = mask.replace("\t", "")
    return mask


def _extract_conjunction(rule, conjunction):
    condition = ""
    listconditions = rule.strip().split("&")
    i = 0
    for s in listconditions:
        # print(s)
        listLabel = s.strip().split("'")
        condition = (
            condition + listLabel[1] + " " + listLabel[2][1 : len(listLabel[2]) - 1]
        )

        if i != len(listconditions) - 1:
            condition = condition + " " + conjunction + " "

        i += 1

    return condition


def _generate_expression(sample, tree, paths, mode):
    rules = {}
    expression = ""
    conjunctor = "AND" if mode == "sql" else "and"
    disjunctor = "OR" if mode == "sql" else "or"

    j = 0
    for key in paths:
        rules[key] = _get_rule(tree, paths[key], sample.columns)
        new_conjunction = _extract_conjunction(rules[key], conjunctor)

        if j == 0:
            expression = "(" + new_conjunction + ")"
        else:
            expression = expression + " " + disjunctor + " (" + new_conjunction + ")"

        j += 1

    return expression


def get_steering_condition(features: pd.DataFrame, labels: pd.DataFrame, mode="pandas"):
    global feature, threshold

    if mode not in ["pandas", "sql"]:
        print("mode must be one of 'pandas' and 'sql'")
        return ""

    classifier = DecisionTreeClassifier(criterion="entropy", max_depth=None)

    print("training tree")
    model = classifier.fit(features, y=labels)
    tree = model.tree_
    feature = tree.feature
    threshold = tree.threshold

    print("extract paths from tree")
    paths = _extract_paths(features, model)

    print("generate conditional expression")
    expression = _generate_expression(features, tree, paths, mode)

    return expression


# adapted from
# https://mljar.com/blog/extract-rules-decision-tree/
def _tree_to_json(tree: BaseDecisionTree, feature_names: list):
    """Transforms a trained tree model from the internal tree format into a simplified, reusable
    python dict."""

    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    feature_names = [f.replace(" ", "_")[:-5] for f in feature_names]

    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"

    def traverse(node, depth):
        __node = ""

        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            __node = (
                f'"type": "internal", "feature": "{name}", "threshold": {threshold}'
            )

            __left = traverse(tree_.children_left[node], depth + 1)
            __node = f'{__node}, "left": {__left}'

            __right = traverse(tree_.children_right[node], depth + 1)
            __node = f'{__node}, "right": {__right}'
        else:
            __node = f'"type": "leaf", "value": {tree_.value[node].tolist()}'

        __node = f"{OPEN_BRACE}{__node}{CLOSE_BRACE}"
        return __node

    __tree = traverse(0, 1)
    __tree = json.loads(__tree)
    return __tree


def get_decision_tree(
    features: pd.DataFrame, labels: pd.DataFrame, use_regression: bool = False
):
    """Helper function for cases where not the steering query, but the model is needed."""
    global feature, threshold

    model = (
        DecisionTreeRegressor(max_depth=5, random_state=0)
        if use_regression
        else DecisionTreeClassifier(criterion="entropy", max_depth=5, random_state=0)
    )

    print("training tree")
    model = model.fit(features, y=labels)
    as_tree = _tree_to_json(model, features.columns)
    return as_tree
