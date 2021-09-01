import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { quadtree } from "./quadtree";
import { getPointsInRect } from "$lib/util/find-in-quadtree";

export const xEncoding = 0;
export const yEncoding = 1;

const vp = {
  minX: 0,
  minY: 0,
  maxX: 1920,
  maxY: 1080
};
export const viewPort = writable(vp);

let currentVisibleData = [] as DataItem[];
export const visibleData = writable(currentVisibleData);

// TODO: if this function is run synchronously, the application crashes on load, due to an error
// with accessing "quadtree" before its declaration.
setTimeout(() => {
  quadtree.subscribe(() => {
    currentVisibleData = getPointsInRect(vp.minX, vp.minY, vp.maxX, vp.maxY);
    visibleData.set(currentVisibleData);
  });
}, 0);