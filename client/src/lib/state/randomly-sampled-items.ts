import type DataItem from "$lib/types/data-item";
import { quadtree } from "./quadtree";
import { writable } from "svelte/store";
import type { Quadtree } from "d3-quadtree";

const iterationsBetweenUpdates = 10;
const sampleSize = 50000

let iteration = 0;
let probability = 1;
let currentQuadtree: Quadtree<DataItem> = null;
let currentProcessedItems: DataItem[] = [];

let sampledItems = [] as DataItem[];
export const randomlySampledItems = writable(sampledItems);


// returns true with a probability such that "sampleSize" items will be retrieved from "items".
// This is done to ensure that the histograms render in acceptable time later in the progression.
function sample() {
  return Math.random() < probability;
};

quadtree.subscribe(newTree => {
  // check if quadtree has changed (for exaxmple when opening the secondary view panel)
  if (iteration % iterationsBetweenUpdates === 0 || currentQuadtree !== newTree) {
    currentProcessedItems = newTree.data();
    probability = sampleSize / currentProcessedItems.length;
    sampledItems = currentProcessedItems.filter(sample);
    randomlySampledItems.set(sampledItems);
    currentQuadtree = newTree;
  }

  if (currentProcessedItems.length > 0) {
    iteration += 1;
  }
});