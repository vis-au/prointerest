import { derived, writable } from "svelte/store";
import { currentTransform } from "./zoom";

export const hoveredPosition = writable([-1, -1] as [number, number]);

export const hoveredScreenPosition = derived(
  [hoveredPosition, currentTransform],
  ([$hoveredPosition, $currentTransform]) => {
    return $currentTransform.apply($hoveredPosition);
  }
);
