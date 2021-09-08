import { getDimensionExtent } from "$lib/util/requests";
import { scaleLinear } from "d3-scale";
import { writable } from "svelte/store";
import { activeViewEncodings } from "./active-view-encodings";

let currentScaleX = scaleLinear();
let currentScaleY = scaleLinear();
let xDimension: string = null;
let yDimension: string = null;
const margin = 0.05;

export const scaleX = writable(currentScaleX);
export const scaleY = writable(currentScaleY);

async function updateScales() {
  if (xDimension === null || yDimension === null) {
    return;
  }

  const xExtent = await getDimensionExtent(xDimension);
  const yExtent = await getDimensionExtent(yDimension);

  const xMargin = (xExtent.max - xExtent.min) * margin;
  xExtent.min = xExtent.min - xMargin;
  xExtent.max = xExtent.max + xMargin;

  const yMargin = (yExtent.max - yExtent.min) * margin;
  yExtent.min = yExtent.min - yMargin;
  yExtent.max = yExtent.max + yMargin;

  currentScaleX.domain([xExtent.min, xExtent.max]);
  currentScaleY.domain([yExtent.min, yExtent.max].reverse());

  scaleX.set(currentScaleX);
  scaleY.set(currentScaleY);
}

activeViewEncodings.subscribe((newEncodings) => {
  xDimension = newEncodings.x;
  yDimension = newEncodings.y;
  updateScales();
});

scaleX.subscribe((scale) => (currentScaleX = scale));
scaleY.subscribe((scale) => (currentScaleY = scale));
