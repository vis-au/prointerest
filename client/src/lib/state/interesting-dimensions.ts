import { writable } from "svelte/store";
import { dimensions } from "./processed-data";

const isDimensionCurrentlyInteresting: Record<string, boolean> = {};
export const isDimensionInteresting = writable(isDimensionCurrentlyInteresting);

const currentIntervals: Record<string, [number, number]> = {};
export const interestingIntervals = writable(currentIntervals);

dimensions.subscribe((dims) => {
  dims.forEach((dim) => {
    isDimensionCurrentlyInteresting[dim] = false;
    currentIntervals[dim] = null;
  });
});
