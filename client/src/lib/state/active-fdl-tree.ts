import type { DecisionTree, InternalNode, LeafNode } from "$lib/types/decision-tree";
import type { DOIDimension } from "$lib/types/doi-dimension";
import { writable } from "svelte/store";
import { interestingIntervals, selectedDoiDimensions } from "./interesting-dimensions";

export const activeFDLTree = writable(null as DecisionTree);

let currentIntervals: Record<DOIDimension, [number, number]> = null
let currentSelectedDoiDimension: DOIDimension[] = [];


function createEmptyInternalNode(): InternalNode {
  return {
    type: "internal",
    feature: null,
    threshold: null,
    left: {
      type: "leaf",
      value: [0]
    },
    right: {
      type: "leaf",
      value: [1]
    }
  };
}

function createTreeFromDimensions(dimensions: DOIDimension[]) {
  const newTree: DecisionTree = createEmptyInternalNode();
  let currentNode = newTree;

  dimensions
    .filter(dimension => currentIntervals[dimension])
    .forEach((dimension, i) => {
      const interval = currentIntervals[dimension]
        ? currentIntervals[dimension]
        : [-Infinity, Infinity];

      currentNode.feature = dimension;
      currentNode.threshold = interval[1];

      (currentNode.right as LeafNode).value = [0];


      currentNode.left = createEmptyInternalNode() as InternalNode;
      currentNode.left.feature = dimension;
      currentNode.left.threshold = interval[0];

      (currentNode.left.left as LeafNode).value = [0];

      if (i < dimensions.length - 1) {
        currentNode.left.right = createEmptyInternalNode();
        currentNode = currentNode.left.right;
      }
    });

  return newTree;
}

function updateFDLTree() {
  if (currentSelectedDoiDimension.length === 0) {
    activeFDLTree.set(null);
    return;
  }

  const rangedDimensions = currentSelectedDoiDimension
    .filter(dimension => currentIntervals[dimension]);

  if (rangedDimensions.length === 0) {
    activeFDLTree.set(null);
    return;
  }

  const newTree = createTreeFromDimensions(rangedDimensions);
  activeFDLTree.set(newTree);
}

interestingIntervals.subscribe(newIntervals => {
  currentIntervals = newIntervals;
  updateFDLTree();
});

selectedDoiDimensions.subscribe(newDimension => {
  currentSelectedDoiDimension = newDimension;
  updateFDLTree();
});