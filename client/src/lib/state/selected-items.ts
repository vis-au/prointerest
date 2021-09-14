import type { HexbinBin } from "d3-hexbin";
import type { ScaleLinear } from "d3-scale";
import { writable } from "svelte/store";

import type DataItem from "$lib/types/data-item";
import { getPointsInPolygon, getPointsInRect } from "$lib/util/find-in-quadtree";
import { activeBrush, activeLasso } from "./active-brush";
import { quadtree } from "./quadtree";
import { selectedBins } from "./selected-bins";
import { scaleX, scaleY } from "./scales";
import type { BrushMode } from "$lib/types/brush-mode";
import { scatterplotBrush } from "./active-scatterplot-brush";

let currentlySelected: DataItem[] = [];
export const selectedItems = writable(currentlySelected);

let currentScatterplotBrush: BrushMode = null;
let currentSelectedBins: HexbinBin<DataItem>[] = [];
let currentBrush: [[number, number], [number, number]] = null;
let currentLasso: [number, number][] = null;
let x: ScaleLinear<number, number> = null;
let y: ScaleLinear<number, number> = null;


function getItemsInRectBrush() {
  const [[x0, y0], [x1, y1]] = currentBrush;
  return getPointsInRect(x(x0), y(y0), x(x1), y(y1));
}

function getItemsInLassoBrush() {
  const scaledPolygon = currentLasso.map(position => {
    return [x.invert(position[0]), y.invert(position[1])] as [number, number];
  });
  return getPointsInPolygon(scaledPolygon);
}

function getBrushedItems() {
  if (x === null || y === null) {
    return [];
  }
  if (currentBrush === null || currentBrush[0] === null) {
    return [];
  }
  if (currentLasso === null) {
    return [];
  }

  return currentScatterplotBrush === "rect"
    ? getItemsInRectBrush()
    : getItemsInLassoBrush();
}

function getItemsInSelectedBins() {
  return currentSelectedBins.map((bin) => bin.slice(0)).flat();
}

function deselectItems() {
  currentlySelected.forEach((item) => (item.selected = false));
}

function getSelectedItems() {
  deselectItems();
  const brushedItems = getBrushedItems();
  const itemsInBins = getItemsInSelectedBins();

  const selected = brushedItems.concat(itemsInBins);
  selected.forEach((d) => (d.selected = true));
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

scatterplotBrush.subscribe((mode) => {
  currentScatterplotBrush = mode;
  updateSelectedItems();
});

activeBrush.subscribe((newBrush) => {
  currentBrush = newBrush;
  updateSelectedItems();
});

activeLasso.subscribe((lasso) => {
  currentLasso = lasso;
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
