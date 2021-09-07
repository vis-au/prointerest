import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { quadtree } from "./quadtree";
import { getPointsInRect } from "$lib/util/find-in-quadtree";

const vp = {
  minX: 0,
  minY: 0,
  maxX: 1920,
  maxY: 1080
};
export const viewPort = writable(vp);

export const visibleData = writable([] as DataItem[]);

// TODO: if this function is run synchronously, the application crashes on load, due to an error
// with accessing "quadtree" before its declaration.
setTimeout(() => {
  quadtree.subscribe(() => {
    const currentVisibleData = getPointsInRect(vp.minX, vp.minY, vp.maxX, vp.maxY);
    visibleData.set(currentVisibleData);
  });
}, 0);
