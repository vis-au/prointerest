import type { Quadtree } from "d3-quadtree";
import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { sample } from "../util/sample";
import { quadtree } from "./quadtree";

const STEPS_BETWEEN_RESAMPLING = 10;
const SAMPLE_SIZE = 50000;

let iteration = 0;
let sampleProbability = 1;

let currentQuadtree: Quadtree<DataItem> = null;
let currentProcessedItems: DataItem[] = [];

let randomSample: DataItem[] = [];
export const randomDataSubset = writable(randomSample);


quadtree?.subscribe((newTree) => {
  // check if actual data in the quadtree has changed or whether items were just repositioned.
  // (for exaxmple when opening the secondary view panel).
  if (iteration % STEPS_BETWEEN_RESAMPLING === 0 || currentQuadtree !== newTree) {
    currentProcessedItems = newTree.data();
    currentQuadtree = newTree;
    sampleProbability = SAMPLE_SIZE / currentProcessedItems.length;

    randomSample = currentProcessedItems.filter(() => sample(sampleProbability));
    randomDataSubset.set(randomSample);
  }

  // this function is called numerous times before any data has actually been loaded, so make sure
  // to adjust the iteration counter only when necessary.
  if (currentProcessedItems.length > 0) {
    iteration += 1;
  }
});
