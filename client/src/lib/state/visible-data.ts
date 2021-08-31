import type { BinType } from "$lib/types/bin-type";
import type { ScaleLinear } from "d3-scale";
import { zoomIdentity } from "d3-zoom";
import { writable } from "svelte/store";
import { processedData } from "./processed-data";
import { scaleX, scaleY } from "./scales";
import { currentTransform } from "./zoom";

export const xEncoding = 0;
export const yEncoding = 1;

let currentScaleX = null as ScaleLinear<number, number>;
let currentScaleY = null as ScaleLinear<number, number>;
let currentT = zoomIdentity;
let currentProcessedData = [] as BinType[];


const vp = {
  minX: 0,
  minY: 0,
  maxX: 1920,
  maxY: 1080
};
export const viewPort = writable(vp);

let currentVisibleData = [] as BinType[];
export const visibleData = writable(currentVisibleData);

function updateVisibleData() {
  currentVisibleData = currentProcessedData.filter(item => {
    const x = currentT.applyX(currentScaleX(item[xEncoding]));
    const y = currentT.applyY(currentScaleY(item[yEncoding]));

    return x > vp.minX && x < vp.maxX && y > vp.minY && y < vp.maxY;
  });

  console.log(currentVisibleData, currentProcessedData, )
  visibleData.set(currentVisibleData);
}


scaleX.subscribe(scale => {
  currentScaleX = scale;
  updateVisibleData();
});
scaleY.subscribe(scale => {
  currentScaleY = scale;
  updateVisibleData();
});
currentTransform.subscribe(newTransform => {
  currentT = newTransform;
  updateVisibleData();
});
processedData.subscribe(newData => {
  currentProcessedData = newData;
  updateVisibleData();
});