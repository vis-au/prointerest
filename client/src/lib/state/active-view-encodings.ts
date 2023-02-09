import type { Encodings } from "$lib/types/encodings";
import { sendAxisDimension } from "$lib/util/requests";
import type { RGBColor } from "d3";
import { writable, type Writable } from "svelte/store";
import { isDimensionInteresting } from "./interesting-dimensions";

export const activeViewEncodings: Writable<Encodings> = writable({
  x: null,
  y: null,
  color: "count",
  size: "count"
});

export const PRIMARY_COLOR: [number, number, number] = [255, 165, 0];
export const HIGHLIGHT_COLOR: [number, number, number] = [0, 128, 128];
export const UNINTERESTING_COLOR: [number, number, number] = [255, 255, 255];

export function colorArrayToRGB(rgbColor: [number, number, number]) {
  return `rgb(${rgbColor[0]}, ${rgbColor[1]}, ${rgbColor[2]})`;
}

export function rgbToColorArray(color: RGBColor) {
  return [color.r, color.g, color.b];
}

activeViewEncodings.subscribe((newEncodings) => {
  if (newEncodings.x !== null) {
    sendAxisDimension("x", newEncodings.x);
    isDimensionInteresting.update((dims) => {
      dims[newEncodings.x] = true;
      return dims;
    });
  }
  if (newEncodings.y !== null) {
    sendAxisDimension("y", newEncodings.y);
    isDimensionInteresting.update((dims) => {
      dims[newEncodings.y] = true;
      return dims;
    });
  }
});
