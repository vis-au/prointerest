import { derived } from "svelte/store";
import { quadtree } from "./quadtree";
import { doiValues } from "./doi-values";
import { doiLimit } from "./doi-limit";


export const items = derived(quadtree, ($quadtree) => {
  if (!$quadtree) {
    return [];
  }

  return $quadtree.data();
});

export const interestingItems = derived(
  [items, doiValues, doiLimit],
  ([$items, $doiValues, $doiLimit]) => {
    return $items.filter((item) => {
      return $doiValues.get(item.id) >= $doiLimit;
    });
  }
);
