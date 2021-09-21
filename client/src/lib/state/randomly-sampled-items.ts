import type { Quadtree } from "d3-quadtree";
import { derived, writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { sample } from "../util/sample-list";
import { quadtree } from "./quadtree";
import { bins } from "./bins";

const iterationsBetweenUpdates = 10;

const currentSmallSampleSize = 1000;
let currentLargeSampleSize = 50000;
export const sampleSize = writable(currentLargeSampleSize);
sampleSize.subscribe((s) => (currentLargeSampleSize = s));

let iteration = 0;
let smallSampleProbabilty = 1;
let largeSampleProbability = 1;

let currentQuadtree: Quadtree<DataItem> = null;
let currentProcessedItems: DataItem[] = [];

let largeRandomSample: DataItem[] = [];
export const randomlySampledItems = writable(largeRandomSample);

let smallRandomSample: DataItem[] = [];
export const lessRandomlySampledItems = writable(smallRandomSample);

// additional set of items that ensure that every bin in the view is at least represented once.
export const randomlySampledBinItems = derived(bins, (newBins) => {
  return newBins
    .map((bin) => {
      const probability = bin.length === 1 ? 1 : smallSampleProbabilty;
      return bin.filter(() => sample(probability));
    })
    .flat();
});

quadtree.subscribe((newTree) => {
  // check if quadtree has changed (for exaxmple when opening the secondary view panel)
  if (iteration % iterationsBetweenUpdates === 0 || currentQuadtree !== newTree) {
    currentProcessedItems = newTree.data();
    currentQuadtree = newTree;
    smallSampleProbabilty = currentSmallSampleSize / currentProcessedItems.length;
    largeSampleProbability = currentLargeSampleSize / currentProcessedItems.length;

    smallRandomSample = currentProcessedItems.filter(() => sample(smallSampleProbabilty));
    largeRandomSample = currentProcessedItems.filter(() => sample(largeSampleProbability));

    lessRandomlySampledItems.set(smallRandomSample);
    randomlySampledItems.set(largeRandomSample);
  }

  if (currentProcessedItems.length > 0) {
    iteration += 1;
  }
});
