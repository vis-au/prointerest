import type { HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";

import type DataItem from "$lib/types/data-item";
import { getPointsInR, getPointsInRect } from "$lib/util/find-in-quadtree";
import { activeBrush } from "./active-brush";
import { quadtree } from "./quadtree";
import { selectedBins } from "./selected-bins";
import { scaleX, scaleY } from "./scales";
import type { ScaleLinear } from "d3-scale";

export const selectedItems = writable([] as DataItem[]);

let currentSelectedBins: HexbinBin<DataItem>[] = [];
let currentBrush: [[number, number], [number, number]] = [
  [-1, -1],
  [-1, -1]
];
let x: ScaleLinear<number, number> = null;
let y: ScaleLinear<number, number> = null;

function getBrushedItems() {
  if (x === null || y === null) {
    return [];
  }
  if (currentBrush === null || currentBrush[0] === null) {
    return [];
  }

  const [[x0, y0], [x1, y1]] = currentBrush;
  return getPointsInRect(x(x0), y(y0), x(x1), y(y1));
}

function getItemsInSelectedBins() {
  return currentSelectedBins.map((bin) => getPointsInR(bin.x, bin.y, 10)).flat();
}

function getSelectedItems() {
  const brushedItems = getBrushedItems();
  const itemsInBins = getItemsInSelectedBins();

  return brushedItems.concat(itemsInBins);
}

scaleX.subscribe((scale) => {
  x = scale;
  selectedItems.set(getSelectedItems());
});
scaleY.subscribe((scale) => {
  y = scale;
  selectedItems.set(getSelectedItems());
});

quadtree.subscribe(() => {
  selectedItems.set(getSelectedItems());
});

activeBrush.subscribe((newBrush) => {
  currentBrush = newBrush;
  selectedItems.set(getSelectedItems());
});

selectedBins.subscribe((newBins) => {
  // optimization to prevent updates of vega lite plots of selected data on zoom
  if (newBins.length === currentSelectedBins.length) {
    return;
  }
  currentSelectedBins = newBins;
  selectedItems.set(getSelectedItems());
});
