import type { Quadtree } from "d3-quadtree";
import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { sample } from "../util/sample";
import { quadtree } from "./quadtree";

const STEPS_BETWEEN_RESAMPLING = 10;

let iteration = 0;
let sampleProbability = 1;

let currentQuadtree: Quadtree<DataItem> = null;
let currentProcessedItems: DataItem[] = [];

let currentSampleSize = 1000;
export const sampleSize = writable(currentSampleSize);
sampleSize.subscribe(newSize => currentSampleSize = newSize);

let currentRandomSample: DataItem[] = [];
export const randomDataSample = writable(currentRandomSample);


quadtree?.subscribe((newTree) => {
  // check if actual data in the quadtree has changed or whether items were just repositioned.
  // (for exaxmple when opening the secondary view panel).
  if (iteration % STEPS_BETWEEN_RESAMPLING === 0 || currentQuadtree !== newTree) {
    currentProcessedItems = newTree.data();
    currentQuadtree = newTree;
    sampleProbability = currentSampleSize / currentProcessedItems.length;

    currentRandomSample = currentProcessedItems.filter(() => sample(sampleProbability));
    randomDataSample.set(currentRandomSample);
  }

  // this function is called numerous times before any data has actually been loaded, so make sure
  // to adjust the iteration counter only when necessary.
  if (currentProcessedItems.length > 0) {
    iteration += 1;
  }
});
