import { createQuadtree } from "$lib/util/create-quadtree";
import { writable } from "svelte/store";
import { smallRandomDataSubset } from "./sampled-data";

let currentSampledQuadtree = createQuadtree();
export const sampledQuadtree = writable(currentSampledQuadtree);

smallRandomDataSubset.subscribe((items) => {
  currentSampledQuadtree = createQuadtree();
  currentSampledQuadtree.addAll(items);
  sampledQuadtree.set(currentSampledQuadtree);
});
