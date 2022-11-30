import { createQuadtree } from "$lib/util/create-quadtree";
import { writable } from "svelte/store";
import { randomDataSubset } from "./sampled-data";

let currentSampledQuadtree = createQuadtree();
export const sampledQuadtree = writable(currentSampledQuadtree);

randomDataSubset.subscribe((items) => {
  currentSampledQuadtree = createQuadtree();
  currentSampledQuadtree.addAll(items);
  sampledQuadtree.set(currentSampledQuadtree);
});
