import { currentTransform } from "$lib/state/zoom";
import type DataItem from "$lib/types/data-item";
import type { ZoomTransform } from "d3";
import { hexbin } from "d3-hexbin";
import { writable } from "svelte/store";

let currentHexbinRadius = 10;
export const hexbinRadius = writable(currentHexbinRadius);

let currentHexBinning = hexbin<DataItem>().radius(currentHexbinRadius);
export const hexbinning = writable(currentHexBinning);

hexbinRadius.subscribe(($hexbinRadius) => {
  currentHexbinRadius = $hexbinRadius;
  currentHexBinning = hexbin<DataItem>().radius(currentHexbinRadius);
  hexbinning.set(currentHexBinning);
});

let transform: ZoomTransform;
currentTransform.subscribe((t) => {
  transform = t;
  currentHexBinning
    .x((d) => transform.applyX(d.position.x))
    .y((d) => transform.applyY(d.position.y));
  hexbinning.set(currentHexBinning);
});
