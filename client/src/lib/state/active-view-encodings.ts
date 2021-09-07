import type { Encodings } from "$lib/types/encodings";
import { sendAxisDimension } from "$lib/util/requests";
import type { Writable } from "svelte/store";
import { writable } from "svelte/store";

export const activeViewEncodings: Writable<Encodings> = writable({
  x: null,
  y: null,
  color: null
});

activeViewEncodings.subscribe((newEncodings) => {
  sendAxisDimension("x", newEncodings.x);
  sendAxisDimension("y", newEncodings.y);
});