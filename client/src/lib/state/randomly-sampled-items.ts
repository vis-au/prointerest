import type DataItem from "$lib/types/data-item";
import { quadtree } from "./quadtree";
import { writable } from "svelte/store";

const iterationsBetweenUpdates = 10;
const sampleSize = 50000
let iteration = 0;

let processedItems: DataItem[] = [];
let probability = 1;

let sampledItems = [] as DataItem[];
export const randomlySampledItems = writable(sampledItems);


// returns true with a probability such that "sampleSize" items will be retrieved from "items".
// This is done to ensure that the histograms render in acceptable time later in the progression.
function sample() {
  return Math.random() < probability;
};

quadtree.subscribe(newTree => {
  processedItems = newTree.data();
  probability = sampleSize / processedItems.length;

  if (iteration % iterationsBetweenUpdates === 0) {
    sampledItems = processedItems.filter(sample);
    randomlySampledItems.set(sampledItems);
  }

  if (processedItems.length > 0) {
    iteration += 1;
  }
});