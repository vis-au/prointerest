import type DataItem from "./data-item";
import type { DOIDimension } from "./doi-dimension"

export type DecisionTree = InternalNode | LeafNode;

export type NodeType = "leaf" | "internal";

export type InternalNode = {
  type: "internal",
  parent?: DecisionTree,
  items?: DataItem[],
  feature: DOIDimension,
  threshold: number,
  left: DecisionTree,
  right: DecisionTree
};

export type LeafNode = {
  type: "leaf",
  parent?: DecisionTree,
  items?: DataItem[],
  value: number[]
};
