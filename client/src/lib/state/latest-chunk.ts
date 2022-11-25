import type DataItem from "$lib/types/data-item";
import { derived, writable } from "svelte/store";
import { doiLimit } from "./doi-limit";
import { doiValues } from "./doi-values";
import { processedData } from "./processed-data";
import { arrayToDataItem } from "./quadtree";
import { scaleX, scaleY } from "./scales";

// stores the "raw" latest chunk as numbers, so that we can respond to changes in the position
// encoding
export const latestChunk = writable([] as number[][]);
let currentLatestChunk: number[][] = [];

// stores the chunk as data items, derived from the raw data
export const latestItems = writable([] as DataItem[]);

// transforms raw data into items, thereby also updating its position.
function updateLatestItems() {
  if (!latestItems || !currentLatestChunk) {
    return;
  }

  latestItems?.set(currentLatestChunk?.map(arrayToDataItem));
}

// whenever the raw data changes, so should the items
latestChunk?.subscribe((newChunk) => {
  currentLatestChunk = newChunk;
  updateLatestItems();
});

scaleX?.subscribe(updateLatestItems);
scaleY?.subscribe(updateLatestItems);


export const latestInterestingItems = derived([doiLimit, latestItems, doiValues], ([$doiLimit, $latestItems, $doiValues]) => {
  return $latestItems.filter((item) => {
    return $doiValues.get(item.id) > $doiLimit;
  });
});

// if the data is cleared/reset, so should be the latest chunk
processedData.subscribe(newData => {
  if (newData.length === 0) {
    latestChunk.set([]);
  }
});
