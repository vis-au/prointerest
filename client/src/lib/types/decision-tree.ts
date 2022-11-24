import type { DOIDimension } from "./doi-dimension"

export type DecisionTree = InternalNode | LeafNode;

export type NodeType = "leaf" | "internal";

export type InternalNode = {
  type: "internal",
  feature: DOIDimension,
  threshold: number,
  left: DecisionTree,
  right: DecisionTree
};

export type LeafNode = {
  type: "leaf",
  value: number[]
};