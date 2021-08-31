import { writable } from "svelte/store";
import type { ZoomTransform } from "d3-zoom";
import { zoomIdentity } from "d3-zoom";

export const currentTransform = writable<ZoomTransform>(zoomIdentity);

export const isZooming = writable(false);