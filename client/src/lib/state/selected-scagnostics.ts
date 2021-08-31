import type { Scagnostic } from "$lib/types/scagnostics";
import { writable } from "svelte/store";

let currentSelectedScagnostics = [] as Scagnostic[];
export const selectedScagnostics = writable(currentSelectedScagnostics);

const weights = new Map<Scagnostic, number>();
export const scagnosticWeights = writable(weights);


selectedScagnostics.subscribe(newSelection => {
  const oldLength = currentSelectedScagnostics.length;
  const newLength = newSelection.length;

  // for simplicity, we assume that either items have been removed or added, but never both.
  if (newLength > oldLength) {
    // new items in selection, so reduce the interest in the existing selection
    const delta = newLength - oldLength;
    const deltaInterest = delta / newLength;
    const reducedInterest = deltaInterest / oldLength;

    // reduce the weight of scagn. already selected
    weights.forEach((value, key) => {
      weights.set(key, value - reducedInterest);
    });

    // find the new items
    const newItems = newSelection.filter(item => {
      return currentSelectedScagnostics.indexOf(item) === -1;
    });

    // set their interest
    newItems.forEach(item => weights.set(item, deltaInterest));

  } else if (newLength === oldLength) {
    // items were removed from the list. Because of the way that writable works, newlength and
    // oldlength are the same here. This means that we need to figure out, how much interest is
    // "missing" from those items, and then add it evenly.
    const outdatedSelection: Scagnostic[] = [];
    weights.forEach((value, key) => {
      outdatedSelection.push(key);
    });

    const deselectedItems = outdatedSelection.filter(item => newSelection.indexOf(item) === -1);

    const delta = deselectedItems
      .map(item => weights.get(item))
      .reduce((a, b) => a+b, 0);
    const increasedInterest = delta / newLength;

    // delete the weights for unselected scagn.
    deselectedItems.forEach(item => weights.delete(item));

    // increase the weights for those that remain
    weights.forEach((value, key) => {
      weights.set(key, value + increasedInterest);
    });
  }

  currentSelectedScagnostics = newSelection;
  scagnosticWeights.set(weights);
});
