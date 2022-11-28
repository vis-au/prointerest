import type { DecisionTree, InternalNode, LeafNode } from "$lib/types/decision-tree";
import type { DOIDimension } from "$lib/types/doi-dimension";
import { writable } from "svelte/store";
import { doiDimensionWeights, interestingIntervals, selectedDoiDimensions } from "./interesting-dimensions";

export const activeFDLTree = writable(null as DecisionTree);

let currentIntervals: Record<DOIDimension, [number, number]> = null
let currentSelectedDoiDimension: DOIDimension[] = [];
let currentDoiWeights: Map<DOIDimension, number> = null;


function createEmptyInternalNode(accumulatedInterest: number): InternalNode {
  return {
    type: "internal",
    feature: null,
    threshold: null,
    left: {
      type: "leaf",
      value: [accumulatedInterest]
    },
    right: {
      type: "leaf",
      value: [accumulatedInterest]
    }
  };
}

function createTreeFromDimensions(dimensions: DOIDimension[]) {
  let accumulatedInterest = 0;
  const newTree: DecisionTree = createEmptyInternalNode(accumulatedInterest);
  let currentNode = newTree;

  dimensions
    .filter(dimension => currentIntervals[dimension])
    .forEach((dimension, i) => {
      const interval = currentIntervals[dimension]
        ? currentIntervals[dimension]
        : [-Infinity, Infinity];

      currentNode.feature = dimension;
      currentNode.threshold = interval[1];

      (currentNode.right as LeafNode).value = [accumulatedInterest];

      console.log(accumulatedInterest, currentDoiWeights)
      accumulatedInterest += currentDoiWeights.get(dimension);

      currentNode.left = createEmptyInternalNode(accumulatedInterest) as InternalNode;
      currentNode.left.feature = dimension;
      currentNode.left.threshold = interval[0];


      if (i < dimensions.length - 1) {
        (currentNode.left.left as LeafNode).value = [accumulatedInterest];
        currentNode.left.right = createEmptyInternalNode(accumulatedInterest);
        currentNode = currentNode.left.right;
      } else {
        (currentNode.left.left as LeafNode).value = [0];
      }
    });

  return newTree;
}

function updateFDLTree() {
  if (currentSelectedDoiDimension.length === 0) {
    activeFDLTree.set(null);
    return;
  }

  const rangedWeightedDimensions = currentSelectedDoiDimension
    .filter(dimension => currentIntervals[dimension])
    .filter(dimension => currentDoiWeights?.has(dimension));

  if (rangedWeightedDimensions.length === 0) {
    activeFDLTree.set(null);
    return;
  }

  const newTree = createTreeFromDimensions(rangedWeightedDimensions);
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

doiDimensionWeights.subscribe(newWeights => {
  currentDoiWeights = newWeights;
  updateFDLTree();
});