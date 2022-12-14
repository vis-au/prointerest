import { derived, writable } from "svelte/store";
import { quadtree } from "./quadtree";
import { doiValues } from "./doi-values";
import { doiLimit } from "./doi-limit";
import type DataItem from "$lib/types/data-item";

export const items = writable([] as DataItem[]);

// this is async to avoid error when loading page caused by access to lexical declaration of quadtr.
setTimeout(() => {
  quadtree?.subscribe(($quadtree) => {
    if (!$quadtree) {
      return;
    }

    items.set($quadtree.data());
  });
}, 0);

export const interestingItems = derived(
  [items, doiValues, doiLimit],
  ([$items, $doiValues, $doiLimit]) => {
    return $items.filter((item) => {
      return $doiValues.get(item.id) >= $doiLimit;
    });
  }
);

export const uninterestingItems = derived(
  [items, doiValues, doiLimit],
  ([$items, $doiValues, $doiLimit]) => {
    return $items.filter((item) => {
      return $doiValues.get(item.id) < $doiLimit;
    });
  }
);
