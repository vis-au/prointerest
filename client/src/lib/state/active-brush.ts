import { writable } from "svelte/store";
import { scatterplotBrush } from "./active-scatterplot-brush";

// brushed coordinates are normalized from the current transform and scales to [0, 1]
export const activeBrush = writable(null as [[number, number], [number, number]]);

export const activeLasso = writable(null as [number, number][]);

// reset the brushes when changing
scatterplotBrush.subscribe(() => {
  activeBrush.set(null);
  activeLasso.set(null);
});
