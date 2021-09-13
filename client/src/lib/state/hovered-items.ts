import type DataItem from "$lib/types/data-item";
import type { HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";
import { bins } from "./bins";
import { hoveredBin } from "./hovered-bin";

export const hoveredItems = writable([] as DataItem[]);

let currentBins = [] as HexbinBin<DataItem>[];
let currentlyHoveredBin = null as HexbinBin<DataItem>;

setTimeout(() => {
  bins.subscribe((b) => {
    currentBins = b;
    updateHoveredItems();
  });
  hoveredBin.subscribe((bin) => {
    currentlyHoveredBin = bin;
    updateHoveredItems();
  });
}, 0);

function updateHoveredItems() {
  if (!currentlyHoveredBin) {
    hoveredItems.set([]);
    return;
  }

  const existingBin = currentBins.find((bin) => {
    return currentlyHoveredBin.x === bin.x && currentlyHoveredBin.y === bin.y;
  });

  if (!existingBin) {
    hoveredItems.set([]);
    return;
  }

  hoveredItems.set(existingBin.slice(0));
}
