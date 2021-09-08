import { writable } from "svelte/store";
import { dimensions } from "./processed-data";

const currentSelection: Record<string, boolean> = {};
export const interestingDimensions = writable(currentSelection);

const currentIntervals: Record<string, [number, number]> = {};
export const interestingIntervals = writable(currentIntervals);

dimensions.subscribe(dims => {
  dims.forEach(dim => {
    currentSelection[dim] = false;
    currentIntervals[dim] = null;
  });
});
