import type DataItem from "$lib/types/data-item";
import { mean } from "d3-array";
import type { HexbinBin } from "d3-hexbin";
import { derived } from "svelte/store";
import { doiValues } from "./doi-values";
import { hexbinning } from "./hexbinning";
import { interestingItems, uninterestingItems } from "./items";
import { randomDataSample } from "./sampled-data";
import { isZooming } from "./zoom";

let currentDoiValues: Map<number, number> = null;
doiValues.subscribe(($doiValues) => (currentDoiValues = $doiValues));

function getAvgDoiInBin(bin: HexbinBin<DataItem>) {
  return mean(bin.map((d) => currentDoiValues.get(d.id)));
}

export const bins = derived(
  [interestingItems, randomDataSample, hexbinning, isZooming],
  ([$interestingItems, $randomDataSample, $hexbinning, $isZooming]) => {
    const bins = $hexbinning($isZooming ? $randomDataSample : $interestingItems);
    bins.forEach((bin) => (bin["doi"] = getAvgDoiInBin(bin)));
    return bins;
  }
);

export const uninterestingBins = derived(
  [uninterestingItems, randomDataSample, hexbinning, isZooming],
  ([$uninterestingItems, $randomDataSample, $hexbinning, $isZooming]) => {
    const bins = $hexbinning($isZooming ? $randomDataSample : $uninterestingItems);
    bins.forEach((bin) => (bin["doi"] = getAvgDoiInBin(bin)));
    return bins;
  }
);
