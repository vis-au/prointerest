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
