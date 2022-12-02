import type { DecisionTree } from "$lib/types/decision-tree";
import { derived, writable } from "svelte/store";

export const selectedDTNode = writable(null as DecisionTree);

export const visibleItemsSelectedInDT = derived([selectedDTNode], ([$selectedDTNode]) => {
  if (!$selectedDTNode) {
    return [];
  }

  return $selectedDTNode.items || [];
});
