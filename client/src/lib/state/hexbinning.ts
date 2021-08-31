import { scaleX, scaleY } from "$lib/state/scales";
import { currentTransform } from "$lib/state/zoom";
import type { BinType } from "$lib/types/bin-type";
import type { ScaleLinear, ZoomTransform } from "d3";
import { hexbin } from "d3-hexbin";
import { writable } from "svelte/store";
import { xEncoding, yEncoding } from "./visible-data";


const currentHexBinning = hexbin<BinType>().radius(10);
export const hexbinning = writable(currentHexBinning);


let currentScaleX: ScaleLinear<number, number>;
let currentScaleY: ScaleLinear<number, number>;
let transform: ZoomTransform;

scaleX.subscribe(scale => {
  currentScaleX = scale;
  currentHexBinning.x(d => transform.applyX(currentScaleX(d[xEncoding])));
  hexbinning.set(currentHexBinning);
});

scaleY.subscribe(scale => {
  currentScaleY = scale;
  currentHexBinning.y(d => transform.applyY(currentScaleY(d[yEncoding])));
  hexbinning.set(currentHexBinning);
});

currentTransform.subscribe(t => {
  transform = t;
  currentHexBinning
    .x(d => t.applyX(currentScaleX(d[xEncoding])))
    .y(d => t.applyY(currentScaleY(d[yEncoding])));
  hexbinning.set(currentHexBinning);
});