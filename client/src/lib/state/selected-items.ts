import type { HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";

import type DataItem from "$lib/types/data-item";
import { getPointsInR, getPointsInRect } from "$lib/util/find-in-quadtree";
import { activeBrush } from "./active-brush";
import { quadtree } from "./quadtree";
import { selectedBins } from "./selected-bins";
import { scaleX, scaleY } from "./scales";
import type { ScaleLinear } from "d3-scale";

let currentlySelected: DataItem[] = [];
export const selectedItems = writable(currentlySelected);

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

function deselectItems() {
  currentlySelected.forEach(item => item.selected = false);
}

function getSelectedItems() {
  deselectItems();
  const brushedItems = getBrushedItems();
  const itemsInBins = getItemsInSelectedBins();

  const selected = brushedItems.concat(itemsInBins);
  selected.forEach(d => d.selected = true);
  return selected;
}

function updateSelectedItems() {
  currentlySelected = getSelectedItems();
  selectedItems.set(currentlySelected);
}

scaleX.subscribe((scale) => {
  x = scale;
  currentlySelected = getSelectedItems();
  updateSelectedItems();
});
scaleY.subscribe((scale) => {
  y = scale;
  updateSelectedItems();
});

quadtree.subscribe(() => {
  updateSelectedItems();
});

activeBrush.subscribe((newBrush) => {
  currentBrush = newBrush;
  updateSelectedItems();
});

selectedBins.subscribe((newBins) => {
  // optimization to prevent updates of vega lite plots of selected data on zoom
  if (newBins.length === currentSelectedBins.length) {
    return;
  }
  currentSelectedBins = newBins;
  updateSelectedItems();
});
