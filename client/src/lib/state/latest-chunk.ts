import type DataItem from "$lib/types/data-item";
import { derived, writable } from "svelte/store";
import { doiLimit } from "./doi-limit";
import { doiValues } from "./doi-values";

export const latestChunk = writable([] as DataItem[]);

export const latestInterestingItems = derived([doiLimit, latestChunk, doiValues], ([$doiLimit, $latestChunk, $doiValues]) => {
  return $latestChunk.filter((item) => {
    return $doiValues.get(item.id) > $doiLimit;
  });
});