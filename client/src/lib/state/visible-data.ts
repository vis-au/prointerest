import { derived, writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { quadtree } from "./quadtree";
import { getPointsInRect } from "$lib/util/find-in-quadtree";
import { doiValues } from "./doi-values";
import { doiLimit } from "./doi-limit";

const vp = {
  minX: 0,
  minY: 0,
  maxX: 1920,
  maxY: 1080
};
export const viewPort = writable(vp);

export const visibleData = writable([] as DataItem[]);

quadtree?.subscribe((newTree) => {
  const currentVisibleData = getPointsInRect(vp.minX, vp.minY, vp.maxX, vp.maxY, newTree);
  visibleData.set(currentVisibleData);
});

export const visibleInterestingData = derived([visibleData, doiValues, doiLimit], ([$visibleData, $doiValues, $doiLimit]) => {
  return $visibleData.filter((item) => {
    return $doiValues.get(item.id) >= $doiLimit;
  });
});