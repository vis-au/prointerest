import type { DOIDimension } from "./doi-dimension"

export type DecisionTree = InternalNode | LeafNode;

export type NodeType = "leaf" | "internal";

export type InternalNode = {
  type: NodeType,
  feature: DOIDimension,
  threshold: number,
  left: DecisionTree,
  right: DecisionTree
};

export type LeafNode = {
  type: NodeType,
  value: number[]
};