import { createQuadtree } from "$lib/util/create-quadtree";
import { writable } from "svelte/store";
import { randomlySampledItems } from "./randomly-sampled-items";

let currentSampledQuadtree = createQuadtree();
export const sampledQuadtree = writable(currentSampledQuadtree);

randomlySampledItems.subscribe(items => {
  currentSampledQuadtree = createQuadtree();
  currentSampledQuadtree.addAll(items);
  sampledQuadtree.set(currentSampledQuadtree);
});