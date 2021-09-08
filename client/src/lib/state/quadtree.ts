import { quadtree as d3_quadtree } from "d3-quadtree";
import type { ScaleLinear } from "d3-scale";
import type DataItem from "$lib/types/data-item";
import { processedData } from "./processed-data";
import { writable } from "svelte/store";
import { scaleX, scaleY } from "./scales";
import { activeViewEncodings } from "./active-view-encodings";
import { dimensions } from "./processed-data";
import { CHUNK_SIZE, resetProgression } from "./progression";
import { isSecondaryViewCollapsed } from "./is-secondary-view-collapsed";

let currentQuadtree = createQuadtree();
export const quadtree = writable(currentQuadtree);

let currentScaleX: ScaleLinear<number, number> = null;
let currentScaleY: ScaleLinear<number, number> = null;

let currentlyProcessedData: number[][];
let currentDimensions: string[] = [];

const idIndex = 0;
let xIndex = -1;
let yIndex = -1;

function createQuadtree() {
  return d3_quadtree<DataItem>()
    .x((d) => d.position.x)
    .y((d) => d.position.y);
}

function insertIntoQuadtree(rawItems: number[][]) {
  const dataItems = !rawItems ? [] : rawItems.map(arrayToDataItem);

  if (dataItems.length === 0) {
    // in case the progression was reset, clear the quadtree as well.
    currentQuadtree = createQuadtree();
  } else {
    // otherwise just add the data to the quadtree
    currentQuadtree.addAll(dataItems);
  }

  quadtree.set(currentQuadtree);
}

function arrayToDataItem(item: number[]) {
  const newItem: DataItem = {
    id: item[idIndex],
    position: {
      x: currentScaleX(item[xIndex]),
      y: currentScaleY(item[yIndex])
    },
    iteration: 0,
    values: item
  };

  return newItem;
}

function recreateQuadtree() {
  const newTree = createQuadtree();
  quadtree.set(newTree);
  insertIntoQuadtree(currentlyProcessedData);
}

// is run asynchronously to ensure that the scales are set
setTimeout(() => {
  processedData.subscribe((newData) => {
    const newItems = newData
      .slice(newData.length - newData.length - CHUNK_SIZE, newData.length);

    insertIntoQuadtree(newItems);

    currentlyProcessedData = newData;
  });
}, 0);

scaleX.subscribe((newScale) => (currentScaleX = newScale));
scaleY.subscribe((newScale) => (currentScaleY = newScale));

dimensions.subscribe((newDims) => (currentDimensions = newDims));

activeViewEncodings.subscribe((newEncodings) => {
  xIndex = currentDimensions.indexOf(newEncodings.x);
  yIndex = currentDimensions.indexOf(newEncodings.y);
  resetProgression();
});

isSecondaryViewCollapsed.subscribe(recreateQuadtree);
