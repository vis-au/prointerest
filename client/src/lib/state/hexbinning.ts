import { currentTransform } from "$lib/state/zoom";
import type DataItem from "$lib/types/data-item";
import type { ZoomTransform } from "d3";
import { hexbin } from "d3-hexbin";
import { writable } from "svelte/store";

let currentHexbinRadius = 10;
export const hexbinRadius = writable(currentHexbinRadius);

const currentHexBinning = hexbin<DataItem>().radius(currentHexbinRadius);
export const hexbinning = writable(currentHexBinning);

function updateHexbinning() {
  currentHexBinning
    .radius(currentHexbinRadius)
    .x((d) => transform.applyX(d.position.x))
    .y((d) => transform.applyY(d.position.y));
  hexbinning.set(currentHexBinning);
}

hexbinRadius.subscribe(($hexbinRadius) => {
  currentHexbinRadius = $hexbinRadius;
  updateHexbinning();
});

let transform: ZoomTransform;
currentTransform.subscribe((t) => {
  transform = t;
  updateHexbinning();
});
