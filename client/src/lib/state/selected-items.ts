import type { HexbinBin } from "d3-hexbin";
import type { Quadtree } from "d3-quadtree";
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
import { visibleItemsSelectedInDT } from "./selection-in-dt";

let currentlySelected: DataItem[] = [];
export const selectedItems = writable(currentlySelected);

let currentBrushedItems: DataItem[] = [];
export const brushedItems = writable(currentBrushedItems);

let currentScatterplotBrush: BrushMode = null;
let currentSelectedBins: HexbinBin<DataItem>[] = [];
let currentSelectedInDT: DataItem[] = [];
let currentBrush: [[number, number], [number, number]] = null;
let currentLasso: [number, number][] = null;
let x: ScaleLinear<number, number> = null;
let y: ScaleLinear<number, number> = null;

let currentQuadtree: Quadtree<DataItem> = null;

quadtree?.subscribe((newTree) => {
  currentQuadtree = newTree;
});

function getItemsInRectBrush() {
  if (currentBrush === null || currentBrush[0] === null) {
    return [];
  }
  const [[x0, y0], [x1, y1]] = currentBrush;
  return getPointsInRect(x(x0), y(y0), x(x1), y(y1), currentQuadtree);
}

function getItemsInLassoBrush() {
  if (currentLasso === null) {
    return [];
  }

  const scaledPolygon = currentLasso.map((position) => {
    return [x(position[0]), y(position[1])] as [number, number];
  });
  return getPointsInPolygon(scaledPolygon, currentQuadtree);
}

function getBrushedItems() {
  if (x === null || y === null) {
    return [];
  }

  return currentScatterplotBrush === "rect" ? getItemsInRectBrush() : getItemsInLassoBrush();
}

function getItemsInSelectedBins() {
  return currentSelectedBins.map((bin) => bin.slice(0)).flat();
}

function deselectItems() {
  currentlySelected.forEach((item) => (item.selected = false));
}

function getSelectedItems() {
  deselectItems();
  const itemsInBins = getItemsInSelectedBins();

  const selected = currentBrushedItems.concat(itemsInBins).concat(currentSelectedInDT);
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

quadtree?.subscribe(() => {
  updateSelectedItems();
});

scatterplotBrush.subscribe((mode) => {
  currentScatterplotBrush = mode;
  currentBrushedItems = getBrushedItems();
  brushedItems.set(currentBrushedItems);
  updateSelectedItems();
});

activeBrush.subscribe((newBrush) => {
  currentBrush = newBrush;
  currentBrushedItems = getBrushedItems();
  brushedItems.set(currentBrushedItems);
  updateSelectedItems();
});

activeLasso.subscribe((lasso) => {
  currentLasso = lasso;
  currentBrushedItems = getBrushedItems();
  brushedItems.set(currentBrushedItems);
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

visibleItemsSelectedInDT.subscribe((newSelection) => {
  currentSelectedInDT = newSelection;
  updateSelectedItems();
});
