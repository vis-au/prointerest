import type { Quadtree } from "d3-quadtree";
import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { sample } from "../util/sampleListRandomly";
import { quadtree } from "./quadtree";


const iterationsBetweenUpdates = 10;

const currentSmallSampleSize = 1000;
let currentLargeSampleSize = 50000;
export const sampleSize = writable(currentLargeSampleSize);
sampleSize.subscribe(s => currentLargeSampleSize = s);

let iteration = 0;
let smallSampleProbabilty = 1;
let largeSampleProbability = 1;

let currentQuadtree: Quadtree<DataItem> = null;
let currentProcessedItems: DataItem[] = [];

let largeRandomSample:  DataItem[] = [];
export const randomlySampledItems = writable(largeRandomSample);

let smallRandomSample: DataItem[] = [];
export const lessRandomlySampledItems = writable(smallRandomSample);

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
