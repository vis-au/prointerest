import type { Quadtree } from "d3-quadtree";
import type { ScaleLinear } from "d3-scale";
import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { createQuadtree } from "$lib/util/create-quadtree";
import { processedData } from "./processed-data";
import { scaleX, scaleY } from "./scales";
import { activeViewEncodings } from "./active-view-encodings";
import { dimensions } from "./processed-data";
import { CHUNK_SIZE } from "./progression";

let currentQuadtree = createQuadtree();
export const quadtree = writable(currentQuadtree);

let currentScaleX: ScaleLinear<number, number> = null;
let currentScaleY: ScaleLinear<number, number> = null;

let currentlyProcessedData: number[][];
let currentDimensions: string[] = [];

const idIndex = 0;
let xIndex = -1;
let yIndex = -1;

function insertIntoQuadtree(tree: Quadtree<DataItem>, rawItems: number[][]) {
  const dataItems = !rawItems ? [] : rawItems.map(arrayToDataItem);

  tree.addAll(dataItems);

  return tree;
}

function arrayToDataItem(item: number[]) {
  const newItem: DataItem = {
    id: item[idIndex],
    position: {
      x: currentScaleX(item[xIndex]),
      y: currentScaleY(item[yIndex])
    },
    selected: false,
    iteration: 0,
    values: item
  };

  return newItem;
}

function recreateQuadtree() {
  const newTree = createQuadtree();
  insertIntoQuadtree(newTree, currentlyProcessedData);
  currentQuadtree = newTree;
  quadtree.set(newTree);
}

// is run asynchronously to ensure that the scales are set
setTimeout(() => {
  processedData.subscribe((newData) => {
    const newItems = newData.slice(newData.length - newData.length - CHUNK_SIZE, newData.length);

    if (newData.length === 0) {
      recreateQuadtree();
    } else {
      insertIntoQuadtree(currentQuadtree, newItems);
      quadtree.set(currentQuadtree);
    }

    currentlyProcessedData = newData;
  });
}, 0);

scaleX.subscribe((newScale) => {
  currentScaleX = newScale;
  recreateQuadtree();
});
scaleY.subscribe((newScale) => {
  currentScaleY = newScale;
  recreateQuadtree();
});

dimensions.subscribe((newDims) => (currentDimensions = newDims));

activeViewEncodings.subscribe((newEncodings) => {
  xIndex = currentDimensions.indexOf(newEncodings.x);
  yIndex = currentDimensions.indexOf(newEncodings.y);
  recreateQuadtree();
});
