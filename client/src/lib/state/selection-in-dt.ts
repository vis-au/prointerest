import type { DecisionTree } from "$lib/types/decision-tree";
import { doesItemFitFilter, getFiltersForDTPath } from "$lib/util/dt-functions";
import { derived, writable } from "svelte/store";
import { doiValues } from "./doi-values";
import { dimensions } from "./processed-data";
import { visibleInterestingData } from "./visible-data";

export const selectionInDT = writable([] as DecisionTree[]); // list of dt nodes

export const dtFilters = derived([selectionInDT], ([$selectionInDT]) => {
  if ($selectionInDT === null || $selectionInDT === undefined || $selectionInDT.length <= 1) {
    return null;
  }

  return getFiltersForDTPath($selectionInDT);
});

export const visibleItemsSelectedInDT = derived(
  [dtFilters, visibleInterestingData, dimensions, doiValues],
  ([$dtFilters, $visibleInterestingData, $dimensions, $doiValues]) => {
    if (!$dtFilters || !$visibleInterestingData || !$dimensions || !$doiValues) {
      return [];
    }

    return $visibleInterestingData.filter(d => doesItemFitFilter(d, $dtFilters, $dimensions));
  }
);
