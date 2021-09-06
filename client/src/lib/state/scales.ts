import type DataItem from '$lib/types/data-item';
import { extent } from 'd3';
import { scaleLinear } from 'd3-scale';
import { writable } from 'svelte/store';
import { activeViewEncodings } from './active-view-encodings';
import { dimensions } from './processed-data';
import { quadtree } from './quadtree';


let currentProcessedData: DataItem[] = [];
let currentDimensions: string[] = [];
let currentScaleX = scaleLinear();
let currentScaleY = scaleLinear();
let xIndex = -1;
let yIndex = -1;

export const scaleX = writable(currentScaleX);
export const scaleY = writable(currentScaleY);


function updateScales() {
  const xValues = currentProcessedData.length === 0
    ? [0, 1]
    : currentProcessedData.map(d => d.values[xIndex]);

  const yValues = currentProcessedData.length === 0
    ? [0, 1]
    : currentProcessedData.map(d => d.values[yIndex]);

  const xExtent = extent(xValues);
  const yExtent = extent(yValues);

  currentScaleX.domain(xExtent)
  currentScaleY.domain(yExtent.reverse());

  scaleX.set(currentScaleX);
  scaleY.set(currentScaleY);
}

setTimeout(() => {
  quadtree.subscribe(newTree => {
    currentProcessedData = newTree.data();

    updateScales();
  });
}, 0);

activeViewEncodings.subscribe(newEncodings => {
  xIndex = currentDimensions.indexOf(newEncodings.x);
  yIndex = currentDimensions.indexOf(newEncodings.y);
  updateScales();
});

dimensions.subscribe(newDims => currentDimensions = newDims);

scaleX.subscribe(scale => currentScaleX = scale);
scaleY.subscribe(scale => currentScaleY = scale);