import type { Encodings } from "$lib/types/encodings";
import { sendAxisDimension } from "$lib/util/requests";
import type { Writable } from "svelte/store";
import { writable } from "svelte/store";
import { isDimensionInteresting } from "./interesting-dimensions";

export const activeViewEncodings: Writable<Encodings> = writable({
  x: null,
  y: null,
  color: null
});

export const PRIMARY_COLOR: [number, number, number] = [255, 165, 0];
export const HIGHLIGHT_COLOR: [number, number, number] = [0, 128, 128];

export function getRGB(rgbColor: [number, number, number]) {
  return `rgb(${rgbColor[0]}, ${rgbColor[1]}, ${rgbColor[2]})`;
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
