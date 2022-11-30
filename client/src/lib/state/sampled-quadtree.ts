import { createQuadtree } from "$lib/util/create-quadtree";
import { writable } from "svelte/store";
import { randomDataSample } from "./sampled-data";

let currentSampledQuadtree = createQuadtree();
export const sampledQuadtree = writable(currentSampledQuadtree);

randomDataSample.subscribe((items) => {
  currentSampledQuadtree = createQuadtree();
  currentSampledQuadtree.addAll(items);
  sampledQuadtree.set(currentSampledQuadtree);
});
