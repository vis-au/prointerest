import type { DOIDimension } from "$lib/types/doi-dimension";
import { sendDimenionWeights } from "$lib/util/requests";
import { writable } from "svelte/store";
import { dimensions } from "./processed-data";

const isDimensionCurrentlyInteresting: Record<string, boolean> = {};
export const isDimensionInteresting = writable(isDimensionCurrentlyInteresting);

const currentIntervals: Record<string, [number, number]> = {};
export const interestingIntervals = writable(currentIntervals);

dimensions.subscribe((dims) => {
  dims.forEach((dim) => {
    isDimensionCurrentlyInteresting[dim] = false;
    currentIntervals[dim] = null;
  });
});

// this list contains the names of dimensions that are marked as "interesting". NOTE: this is not
// derived from isDimensionInteresting, because that breaks the linking from header to bottom
// components.
let currentlySelectedDoiDimensions = [] as DOIDimension[];
export const selectedDoiDimensions = writable(currentlySelectedDoiDimensions);

// the weights assigned to dimensions in the DOI function
const weights = new Map<DOIDimension, number>();
export const doiDimensionWeights = writable(weights);

selectedDoiDimensions.subscribe((newSelection) => {
  const oldLength = currentlySelectedDoiDimensions.length;
  const newLength = newSelection.length;

  // for simplicity, we assume that either items have been removed or added, but never both.
  if (newLength > oldLength) {
    // new items in selection, so reduce the interest in the existing selection
    const newElements = newLength - oldLength;

    const oldWeight = oldLength / newLength;
    const newWeight = newElements / newLength;

    //
    const equalWeightInNew = 1 / newElements;

    // reduce the weight of scagn. already selected
    weights.forEach((value, key) => {
      weights.set(key, value * oldWeight);
    });

    // find the new items
    const newItems = newSelection.filter((item) => {
      return currentlySelectedDoiDimensions.indexOf(item) === -1;
    });

    // set their interest
    newItems.forEach((item) => weights.set(item, newWeight * equalWeightInNew));
  } else {
    // get the leftover interest sum
    const newSum = newSelection.map((item) => weights.get(item)).reduce((a, b) => a + b, 0);

    // normalize leftover entries to new total interest sum
    newSelection.forEach((item) => weights.set(item, weights.get(item) / newSum));

    // delete the weights for deselected scagn.
    currentlySelectedDoiDimensions
      .filter((item) => newSelection.indexOf(item) === -1)
      .forEach((item) => weights.delete(item));
  }

  currentlySelectedDoiDimensions = newSelection;
  sendDimenionWeights(weights);
  doiDimensionWeights.set(weights);
});