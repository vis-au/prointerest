import type { DecisionTree, InternalNode } from "$lib/types/decision-tree";
import type { DimensionFilter } from "$lib/types/steering-filters";
import { derived, writable } from "svelte/store";
import { doiValues } from "./doi-values";
import { dimensions } from "./processed-data";
import { visibleInterestingData } from "./visible-data";

export const selectionInDT = writable([] as DecisionTree[]); // list of dt nodes

export const dtFilters = derived([selectionInDT], ([$selectionInDT]) => {
  if ($selectionInDT === null || $selectionInDT === undefined || $selectionInDT.length <= 1) {
    return null;
  }

  const filters: DimensionFilter = {};

  // transform consecutive nodes into interval filters
  $selectionInDT.forEach((node) => {
    const predecessor = $selectionInDT.find(
      (d) => d.type === "internal" && (d.left === node || d.right === node)
    ) as InternalNode;

    if (!predecessor) {
      return;
    }

    if (predecessor.left === node) {
      const interval = filters[predecessor.feature] || [null, null];
      interval[1] = predecessor.threshold;
      filters[predecessor.feature] = interval;
    }
    if (predecessor.right === node) {
      const interval = filters[predecessor.feature] || [null, null];
      interval[0] = predecessor.threshold;
      filters[predecessor.feature] = interval;
    }
  });

  // if both sides of a subtree are included, remove the filter
  for (const dimension in filters) {
    if (filters[dimension][0] === filters[dimension][1]) {
      delete filters[dimension];
    }
  }

  return filters;
});

export const visibleItemsSelectedInDT = derived(
  [dtFilters, visibleInterestingData, dimensions, doiValues],
  ([$dtFilters, $visibleInterestingData, $dimensions, $doiValues]) => {
    if (!$dtFilters || !$visibleInterestingData || !$dimensions || !$doiValues) {
      return [];
    }

    return $visibleInterestingData.filter((item) => {
      let matchesFilters = true;

      // apply the filters defined by the brushes in the
      Object.keys($dtFilters).forEach((dimension) => {
        const index = $dimensions.indexOf(dimension);

        if ($dtFilters[dimension][0]) {
          matchesFilters = matchesFilters && item.values[index] >= $dtFilters[dimension][0];
        }
        if ($dtFilters[dimension][1]) {
          matchesFilters = matchesFilters && item.values[index] <= $dtFilters[dimension][1];
        }
      });

      return matchesFilters;
    });
  }
);
