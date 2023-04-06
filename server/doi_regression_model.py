import math
from dataclasses import dataclass
from copy import deepcopy

import numpy as np
import pandas as pd
from database import ID, update_dois
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


def get_least_interesting_leaf_node(tree: dict):
    all_leaf_nodes = get_leaf_nodes(tree)

    i_least_interesting = min(enumerate(all_leaf_nodes), key=lambda x: x[1].interest)[0]
    return all_leaf_nodes[i_least_interesting]


class DoiRegressionModel:
    storage: StorageStrategy  # access to items in the database
    tree: DecisionTreeRegressor  # model used of the data based on DOI function
    validity_threshold: float  # ABOVE IS GOOD, BELOW IS BAD
    interest_threshold: float  # ABOVE IS INTERESTING, BELOW IS NOT
    include_previous_chunks_in_training: bool = (
        True  # retrain on historic results or not?
    )
    update_all_dois_after_retraining: bool = (
        True  # should "old" values be updated with new model?
    )
    trained_column_labels: "list[str]" = []
    all_column_labels: "list[str]" = []
    outdated_items: pd.DataFrame
    updated_dois: np.ndarray

    def __init__(
        self,
        storage: StorageStrategy,
        max_depth: int = 3,
        validity_threshold: float = 0.95,
        interest_threshold: int = 0.75,
        include_previous_chunks_in_training: bool = False
    ) -> None:
        self.storage = storage
        self.tree = DecisionTreeRegressor(max_depth=max_depth)
        self.validity_threshold = validity_threshold
        self.interest_threshold = interest_threshold
        self.include_previous_chunks_in_training = include_previous_chunks_in_training

    def __str__(self) -> str:
        return str(_tree_to_json(self.tree, self.trained_column_labels))

    def _get_leaf_nodes(self):
        """Simple wrapper function for getting to the leaf nodes."""
        tree_as_dict = _tree_to_json(self.tree, self.trained_column_labels)
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

    def _get_stratified_context(self, n: int) -> pd.DataFrame:
        """Samples a maximum of n/|leafs| from each leaf node into the context."""
        leaf_nodes = self._get_leaf_nodes()
        n_items_per_leaf = math.ceil(n / len(leaf_nodes))

        context_items = []
        for leaf_node in leaf_nodes:
            context_items += [
                self._get_n_items_for_leaf_node(n_items_per_leaf, leaf_node)
            ]

        context_items = pd.concat(context_items)

        return context_items

    def _get_min_max_context(self, n: int) -> pd.DataFrame:
        """Samples half from the leaf with maximum value and half from leaf with minimum value."""
        n_items_per_leaf = math.ceil(n / 2)
        tree_as_dict = _tree_to_json(self.tree, self.trained_column_labels)

        min_doi_leaf = get_least_interesting_leaf_node(tree_as_dict)
        max_doi_leaf = get_most_interest_leaf_node(tree_as_dict)

        min_doi_items = self._get_n_items_for_leaf_node(n_items_per_leaf, min_doi_leaf)
        max_doi_items = self._get_n_items_for_leaf_node(n_items_per_leaf, max_doi_leaf)

        context_items = pd.concat([min_doi_items, max_doi_items], ignore_index=True)

        return context_items

    def _get_outdated_items(
        self, new_tree: DecisionTreeRegressor, old_tree: DecisionTreeRegressor
    ) -> pd.DataFrame:
        """Identify those branches in the tree model that are no longer valid (error too large) and
        return all items that match them."""
        leaf_nodes = self._get_leaf_nodes()
        SAMPLE_SIZE = 1000

        outdated_df = pd.DataFrame([], columns=self.all_column_labels)

        # determine, which items are affected by this retraining
        for leaf_node in leaf_nodes:
            sample = self._get_n_items_for_leaf_node(SAMPLE_SIZE, leaf_node)
            score = self.score(
                sample, new_tree.predict(sample.select_dtypes(include=[np.number]))
            )

            if score < self.validity_threshold:
                # has to include the ID dimension for retrieval in upstream functions
                outdated_df = pd.concat([outdated_df, sample], ignore_index=True)

        return outdated_df

    def _train(self, df: pd.DataFrame, dois: np.ndarray) -> None:
        assert df.shape[0] == len(dois)

        self.all_column_labels = df.columns
        numeric_df = df.select_dtypes(include=[np.number])
        self.trained_column_labels = numeric_df.columns
        outdated_tree = deepcopy(self.tree)

        # hasattr checks if the prior model is trained
        if self.include_previous_chunks_in_training and hasattr(self.tree, "tree_"):
        #     # retraining strategy 1: include context and predicted doi in training
        #     # FIXME: uses same size as chunk size for training
        #     context_df = self.get_context_items(len(df))
        #     context_df = context_df.select_dtypes(include=[np.number])
        #     context_dois = self.predict_doi(context_df).reshape((-1,))
        #     dois = dois.reshape((-1,))

        #     training_df = pd.concat([numeric_df, context_df], ignore_index=True)
        #     training_dois = np.concatenate([dois, context_dois], axis=0)
        #     self.tree.fit(training_df, training_dois)
        # elif hasattr(self.tree, "tree_"):
            # retraining strategy 2: predict the doi with the current model and include the weighted
            # sum as training labels
            prior_dois = self.predict_doi(numeric_df).reshape((-1,))
            dois = dois.reshape((-1, ))
            training_dois = (dois + prior_dois) / 2
            self.tree.fit(numeric_df, training_dois)
        else:
            self.tree.fit(numeric_df, dois)

        return self.tree, outdated_tree

    def _repredict_all_dois(self) -> None:
        outdated_items = self.storage.get_available_items()
        outdated_ids = outdated_items[ID]
        outdated_items = outdated_items.select_dtypes(include=[np.number])

        new_dois = self.tree.predict(outdated_items)
        update_dois(ids=outdated_ids.tolist(), dois=new_dois.tolist())

        return outdated_ids, new_dois

    def _repredict_outdated_dois(
        self, updated_tree: DecisionTreeRegressor, outdated_tree: DecisionTreeRegressor
    ) -> None:
        outdated_df = self._get_outdated_items(updated_tree, outdated_tree)
        outdated_ids = outdated_df[ID]
        outdated_df = outdated_df.select_dtypes(include=[np.number])
        new_dois = np.array([]).reshape((-1,))

        if len(outdated_df) > 0:
            new_dois = self.predict_doi(outdated_df)
            update_dois(ids=outdated_ids.tolist(), dois=new_dois.tolist())

        return outdated_df, new_dois

    def update(
        self, new_df: pd.DataFrame, new_dois: np.ndarray, update_outdated: bool = False
    ) -> None:
        updated_tree, outdated_tree = self._train(new_df, new_dois)
        if update_outdated:
            # self._repredict_all_dois(updated_tree, outdated_tree)
            outdated_df, new_dois = self._repredict_outdated_dois(
                updated_tree, outdated_tree
            )
            self.outdated_items = outdated_df
            self.updated_dois = new_dois

    def score(self, new_df: pd.DataFrame, new_dois: np.ndarray):
        assert new_df.shape[0] == len(new_dois)

        # R^2 scores is not well-defined with less than two samples
        if len(new_df) < 2:
            return 1

        numeric_df = new_df.select_dtypes(include=[np.number])
        return self.tree.score(numeric_df, new_dois)

    def predict_doi(self, df: pd.DataFrame):
        numeric_df = df.select_dtypes(include=[np.number])
        return self.tree.predict(numeric_df)

    def get_context_items(self, n: int, strategy: str = "stratified") -> pd.DataFrame:
        if strategy == "stratified":
            return self._get_stratified_context(n)
        elif strategy == "minmax":
            return self._get_min_max_context(n)
