import { writable } from "svelte/store";

const vp = {
  minX: 0,
  minY: 0,
  maxX: 1920,
  maxY: 1080
};

export const viewPort = writable(vp);

export function isPointInView(x: number, y: number, padding=0) {
  return x - padding > vp.minX
    && x + padding < vp.maxX
    && y - padding > vp.minY
    && y + padding < vp.maxY;
}
