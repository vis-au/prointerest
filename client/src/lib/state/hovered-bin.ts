import type DataItem from "$lib/types/data-item";
import { getDummyDataItem } from "$lib/util/dummy-data-item";
import type { Hexbin, HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";
import { hoveredPosition } from "./hovered-position";
import { hexbinning } from "./hexbinning";

let currentlyHoveredBin = null as HexbinBin<DataItem>;
export const hoveredBin = writable(null as HexbinBin<DataItem>);

let currentHexbinning = null as Hexbin<DataItem>;
let currentlyHoveredPosition = null as [number, number];


setTimeout(() => {
  hoveredPosition.subscribe(position => {
    currentlyHoveredPosition = position;
    updateHoveredBin();
  });
  hexbinning.subscribe(h => currentHexbinning = h);
}, 0);

function updateHoveredBin() {
  if (!currentlyHoveredPosition || !currentHexbinning) {
    hoveredBin.set(null);
    return;
  }

  const dummyItem = getDummyDataItem();
  dummyItem.position.x = currentlyHoveredPosition[0];
  dummyItem.position.y = currentlyHoveredPosition[1];
  currentlyHoveredBin = currentHexbinning([dummyItem])[0];

  if (!currentlyHoveredBin) {
    currentlyHoveredBin = null;
    hoveredBin.set(null);
    return;
  }

  hoveredBin.set(currentlyHoveredBin);
}