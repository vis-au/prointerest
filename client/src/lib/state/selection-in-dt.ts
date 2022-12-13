import type { DecisionTree } from "$lib/types/decision-tree";
import { derived, writable } from "svelte/store";
import { isSecondaryViewCollapsed } from "./is-secondary-view-collapsed";

export const selectedDTNode = writable(null as DecisionTree);

export const activeDTPath = writable([] as DecisionTree[]);

export const visibleItemsSelectedInDT = derived([selectedDTNode], ([$selectedDTNode]) => {
  if (!$selectedDTNode) {
    return [];
  }

  return $selectedDTNode.items || [];
});

isSecondaryViewCollapsed.subscribe(() => {
  // FIXME: items in visibleItemsSelectedInDT become outdated when the view changes, so the
  // highlighted bins are invalid. As a hotfix, the selected node is simply deselected here,
  // whenever the secondary view is toggled.
  selectedDTNode.set(null);
  activeDTPath.set([]);
});
