import type { Quadtree } from "d3-quadtree";
import { derived, writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { sample } from "../util/sample";
import { quadtree } from "./quadtree";
import { bins } from "./bins";

const STEPS_BETWEEN_RESAMPLING = 10;

const SMALL_SAMPLE_SIZE = 1000;
const LARGE_SAMPLE_SIZE = 50000;

let iteration = 0;
let smallSampleProbabilty = 1;
let largeSampleProbability = 1;

let currentQuadtree: Quadtree<DataItem> = null;
let currentProcessedItems: DataItem[] = [];

let largeRandomSample: DataItem[] = [];
export const randomDataSubset = writable(largeRandomSample);

let smallRandomSample: DataItem[] = [];
export const smallRandomDataSubset = writable(smallRandomSample);

// additional set of items that ensure that every bin in the view is at least represented once.
export const randomlySampledBinItems = derived(bins, ($bins) => {
  return $bins
    .map((bin) => {
      const probability = bin.length === 1 ? 2 : smallSampleProbabilty;
      return bin.filter(() => sample(probability));
    })
    .flat();
});

quadtree?.subscribe((newTree) => {
  // check if actual data in the quadtree has changed or whether items were just repositioned.
  // (for exaxmple when opening the secondary view panel).
  if (iteration % STEPS_BETWEEN_RESAMPLING === 0 || currentQuadtree !== newTree) {
    currentProcessedItems = newTree.data();
    currentQuadtree = newTree;
    smallSampleProbabilty = SMALL_SAMPLE_SIZE / currentProcessedItems.length;
    largeSampleProbability = LARGE_SAMPLE_SIZE / currentProcessedItems.length;

    smallRandomSample = currentProcessedItems.filter(() => sample(smallSampleProbabilty));
    largeRandomSample = currentProcessedItems.filter(() => sample(largeSampleProbability));

    smallRandomDataSubset.set(smallRandomSample);
    randomDataSubset.set(largeRandomSample);
  }

  // this function is called numerous times before any data has actually been loaded, so make sure
  // to adjust the iteration counter only when necessary.
  if (currentProcessedItems.length > 0) {
    iteration += 1;
  }
});
