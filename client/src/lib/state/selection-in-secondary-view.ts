import type { DimensionFilter } from "$lib/types/steering-filters";
import { derived, writable } from "svelte/store";
import { doiValues } from "./doi-values";
import { dimensions } from "./processed-data";
import { visibleInterestingData } from "./visible-data";

export const selectionInSecondaryView = writable({} as DimensionFilter);

export const visibleItemsSelectedInSecondaryView = derived(
  [selectionInSecondaryView, visibleInterestingData, dimensions, doiValues],
  ([$selectionInSecondaryView, $visibleInterestingData, $dimensions, $doiValues]) => {
    return $visibleInterestingData.filter((item) => {
      // if no filter is active, no items are selected (even though technically everything matches)
      let matchesFilter = Object.keys($selectionInSecondaryView).length > 0;

      // apply the filters defined by the brushes in the
      Object.keys($selectionInSecondaryView).forEach((dimension) => {
        const interval = $selectionInSecondaryView[dimension];
        const index = $dimensions.indexOf(dimension);

        // doi is not part of values, but requires lookup instead
        if (dimension === "doi") {
          matchesFilter =
            matchesFilter &&
            $doiValues.get(item.id) >= interval[0] &&
            $doiValues.get(item.id) <= interval[1];
        } else {
          matchesFilter =
            matchesFilter && item.values[index] >= interval[0] && item.values[index] <= interval[1];
        }
      });

      return matchesFilter;
    });
  }
);
