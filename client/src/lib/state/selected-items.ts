import type { BinType } from "$lib/types/bin-type";
import type { ScaleLinear } from "d3";
import { writable } from "svelte/store";
import { activeBrush } from "./active-brush";
import { processedData } from "./processed-data";
import { scaleX, scaleY } from "./scales";

export const selectedItems = writable([] as BinType[]);

let currentProcessedData: BinType[] = [];
let currentBrush: [[number, number], [number, number]] = [[-1, -1], [-1, -1]];
let currentScaleX: ScaleLinear<number, number> = null;
let currentScaleY: ScaleLinear<number, number> = null;

function findSelectedItems() {
  if (currentScaleX === null || currentScaleY === null) {
    return [];
  }

  const [[x0, y0], [x1, y1]] = currentBrush;
  const minX = currentScaleX.invert(x0);
  const minY = currentScaleY.invert(y0);
  const maxX = currentScaleX.invert(x1);
  const maxY = currentScaleY.invert(y1);

  return currentProcessedData.filter(item => {
    return item[0] >= minX && item[0] <= maxX && item[1] >= minY && item[1] <= maxY;
  });
}

processedData.subscribe(newData => {
  currentProcessedData = newData;
  selectedItems.set(findSelectedItems());
});

activeBrush.subscribe(newBrush => {
  currentBrush = newBrush;
  selectedItems.set(findSelectedItems());
});

scaleX.subscribe(newScale => {
  currentScaleX = newScale;
});

scaleY.subscribe(newScale => {
  currentScaleY = newScale;
});