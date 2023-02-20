from dataclasses import dataclass

import numpy as np
import pandas as pd
import math
from sklearn.tree import DecisionTreeRegressor
from steering import _tree_to_json
from storage_strategy.storage_strategy import StorageStrategy


@dataclass
class DecisionRule:
    feature: str
    min: int or float = None
    max: int or float = None


@dataclass
class LeafNode:
    decision_rules: "list[DecisionRule]"
    interest: float

    def get_query(self, table_name: str = ""):
        query = ""

        for rule in self.decision_rules:
            # add conjunction to previous filters
            if len(query) > 0:
                query += " AND "

            # optionally qualify the table the query operates
            if table_name:
                query += table_name + "."

            # add decision rule as filter
            if rule.min is None:
                query += f"{rule.feature} <= {rule.max}"
            elif rule.max is None:
                query += f"{rule.feature} > {rule.min}"

        return query


def get_leaf_nodes(tree: dict) -> "list[LeafNode]":
    def traverse(node: dict, path: "list[DecisionRule]"):
        if node["type"] == "internal":
            rule_left = DecisionRule(feature=node["feature"], max=node["threshold"])
            left = traverse(node["left"], path + [rule_left])

            rule_right = DecisionRule(feature=node["feature"], min=node["threshold"])
            right = traverse(node["right"], path + [rule_right])

            return left + right  # avoid tested lists in result
        else:
            return [LeafNode(interest=node["value"][0][0], decision_rules=path)]

    return traverse(tree, [])


def get_interesting_leaf_nodes(tree: dict, threshold: float):
    def is_leaf_node_interesting(leaf_node: LeafNode):
        return leaf_node.interest >= threshold

    all_leaf_nodes = get_leaf_nodes(tree)
    interesting_leaf_nodes = list(filter(is_leaf_node_interesting, all_leaf_nodes))
    return interesting_leaf_nodes


def get_query_to_interesting_leaf_nodes(
    tree: dict, threshold: float, table_name: str = ""
):
    interesting_leaf_nodes = get_interesting_leaf_nodes(tree, threshold)

    interesting_query = ""
    for leaf_node in interesting_leaf_nodes:
        if len(interesting_query) > 0:
            interesting_query += " OR "
        interesting_query += f"({leaf_node.get_query(table_name)})"

    return interesting_query


def get_most_interest_leaf_node(tree: dict):
    all_leaf_nodes = get_leaf_nodes(tree)

    i_most_interesting = max(enumerate(all_leaf_nodes), key=lambda x: x[1].interest)[0]
    return all_leaf_nodes[i_most_interesting]


class DoiRegressionModel:
    storage: StorageStrategy  # access to items in the database
    tree: DecisionTreeRegressor  # model used of the data based on DOI function
    validity_threshold: float  # ABOVE IS GOOD, BELOW IS BAD
    interest_threshold: float  # ABOVE IS INTERESTING, BELOW IS NOT
    column_labels: "list[str]" = []

    def __init__(
        self,
        storage: StorageStrategy,
        max_depth: int = 3,
        validity_threshold: float = 0.8,
        interest_threshold: int = 0.75,
    ) -> None:
        self.storage = storage
        self.tree = DecisionTreeRegressor(max_depth=max_depth)
        self.validity_threshold = validity_threshold
        self.interest_threshold = interest_threshold

    def __str__(self) -> str:
        return str(_tree_to_json(self.tree, self.column_labels))

    def _get_leaf_nodes(self):
        """Simple wrapper function for getting to the leaf nodes."""
        tree_as_dict = _tree_to_json(self.tree, self.column_labels)
        leaf_nodes = get_leaf_nodes(tree_as_dict)
        return leaf_nodes

    def _is_still_valid(self, new_df: pd.DataFrame, new_dois: np.ndarray) -> bool:
        """
        Evaluate the regression model by comparing its prediction against actual DOI values (R**2).
        """

        score = self.score(new_df, new_dois)
        return score >= self.validity_threshold

    def _get_n_items_for_leaf_node(self, n: int, leaf_node: LeafNode):
        query = leaf_node.get_query()
        return self.storage.get_n_items_from_query(query, n)

    def _get_all_items_for_leaf_node(self, leaf_node: LeafNode):
        query = leaf_node.get_query()
        return self.storage.get_n_items_from_query(query)

    def _train(self, df: pd.DataFrame, dois: np.ndarray) -> None:
        assert df.shape[0] == len(dois)
        self.column_labels = df.columns
        self.tree.fit(df, dois)

    def update(self, new_df: pd.DataFrame, new_dois: np.ndarray) -> None:
        self._train(new_df, new_dois)

    def score(self, new_df: pd.DataFrame, new_dois: np.ndarray):
        assert new_df.shape[0] == len(new_dois)
        return self.tree.score(new_df, new_dois)

    def predict_doi(self, df: pd.DataFrame):
        return self.tree.predict(df)

    def get_context_items(self, n: int) -> pd.DataFrame:
        leaf_nodes = self._get_leaf_nodes()
        n_items_per_leaf = math.ceil(n / len(leaf_nodes))

        context_items = []
        for leaf_node in leaf_nodes:
            context_items += [
                self._get_n_items_for_leaf_node(n_items_per_leaf, leaf_node)
            ]

        context_items = pd.concat(context_items)

        return context_items

    def get_outdated_items(
        self, new_df: pd.DataFrame, new_dois: np.ndarray
    ) -> pd.DataFrame:
        """
        Identify those branches in the tree model that are no longer valid (error too large) and
        return all items that match them.
        """

        # if the model overall is still valid, no need to do anything
        if not self._is_still_valid(new_df, new_dois):
            return []

        leaf_nodes = self._get_leaf_nodes()
        SAMPLE_SIZE = 1000

        # TODO: get the data assigned to each leaf node and score the prediction
        # TODO: return a list of all leaf nodes that are performing below the threshold

        new_tree = self.tree.copy()

        # TODO: train on new data+context!
        new_tree.train(new_df, new_dois)

        outdated_df = pd.DataFrame([], columns=new_df.columns)

        # determine, which items are affected by this retraining
        for leaf_node in leaf_nodes:
            sample = self._get_n_items_for_leaf_node(SAMPLE_SIZE, leaf_node)
            score = self.score(sample, new_tree.predict(sample))

            if score < self.validity_threshold:
                outdated_df = pd.concat(outdated_df, sample, ignore_index=True)

        self.tree = new_tree
        return outdated_df
