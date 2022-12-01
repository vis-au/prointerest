import type { DimensionFilter } from "$lib/types/steering-filters";
import { derived, writable } from "svelte/store";
import { dimensions } from "./processed-data";
import { visibleInterestingData } from "./visible-data";

export const selectionInSecondaryView = writable({} as DimensionFilter);

export const visibleItemsSelectedInSecondaryView =
  derived([selectionInSecondaryView, visibleInterestingData, dimensions], ([$selectionInSecondaryView, $visibleInterestingData, $dimensions]) => {
    return $visibleInterestingData
      .filter(item => {
        // if no filter is active, no items are selected (even though technically everything matches)
        let matchesFilter = Object.keys($selectionInSecondaryView).length > 0;

        // apply the filters defined by the brushes in the
        Object.keys($selectionInSecondaryView).forEach(dimension => {
          const interval = $selectionInSecondaryView[dimension];
          const index = $dimensions.indexOf(dimension);

          matchesFilter = matchesFilter &&
            item.values[index] >= interval[0] &&
            item.values[index] <= interval[1];
        });

        return matchesFilter;
      });
  });
