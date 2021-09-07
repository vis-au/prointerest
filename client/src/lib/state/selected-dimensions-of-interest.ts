import { writable } from "svelte/store";
import { dimensions } from "./processed-data";

const currentSelection: Record<string, boolean> = {};
export const dimensionInterestRecord = writable(currentSelection);

dimensions.subscribe(dims => {
  dims.map(dim => currentSelection[dim] = false);
});
