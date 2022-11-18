import type DataItem from "$lib/types/data-item";
import { derived, writable } from "svelte/store";
import { doiLimit } from "./doi-limit";
import { doiValues } from "./doi-values";
import { processedData } from "./processed-data";

export const latestChunk = writable([] as DataItem[]);

export const latestInterestingItems = derived([doiLimit, latestChunk, doiValues], ([$doiLimit, $latestChunk, $doiValues]) => {
  return $latestChunk.filter((item) => {
    return $doiValues.get(item.id) > $doiLimit;
  });
});

// if the data is cleared/reset, so should be the latest chunk
processedData.subscribe(newData => {
  if (newData.length === 0) {
    latestChunk.set([]);
  }
});
