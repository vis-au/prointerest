import { writable } from "svelte/store";

const vp = {
  minX: 0,
  minY: 0,
  maxX: 1920,
  maxY: 1080
};

export const viewPort = writable(vp);
