import type { Scagnostic } from "$lib/types/scagnostics";
import { sendScagnosticWeights } from "$lib/util/requests";
import { writable } from "svelte/store";

let currentSelectedScagnostics = ["outlying", "clumpy", "stringy"] as Scagnostic[];
export const selectedScagnostics = writable(currentSelectedScagnostics);

const weights = new Map<Scagnostic, number>();
currentSelectedScagnostics.forEach((s) => weights.set(s, 0.3));
export const scagnosticWeights = writable(weights);

selectedScagnostics.subscribe((newSelection) => {
  const oldLength = currentSelectedScagnostics.length;
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
      return currentSelectedScagnostics.indexOf(item) === -1;
    });

    // set their interest
    newItems.forEach((item) => weights.set(item, newWeight * equalWeightInNew));
  } else {
    // get the leftover interest sum
    const newSum = newSelection.map((item) => weights.get(item)).reduce((a, b) => a + b, 0);

    // normalize leftover entries to new total interest sum
    newSelection.forEach((item) => weights.set(item, weights.get(item) / newSum));

    // delete the weights for deselected scagn.
    currentSelectedScagnostics
      .filter((item) => newSelection.indexOf(item) === -1)
      .forEach((item) => weights.delete(item));
  }

  currentSelectedScagnostics = newSelection;
  sendScagnosticWeights(weights);
  scagnosticWeights.set(weights);
});
