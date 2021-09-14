import { writable } from "svelte/store";

// brushed coordinates are normalized from the current transform and scales to [0, 1]
export const activeBrush = writable(null as [[number, number], [number, number]]);

export const activeLasso = writable(null as [number, number][]);
