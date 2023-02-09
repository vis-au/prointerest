import { getAvgDoiInBin } from "$lib/util/avg-doi-in-bin";
import { derived } from "svelte/store";
import { hexbinning } from "./hexbinning";
import { interestingItems, uninterestingItems } from "./items";
import { randomDataSample } from "./sampled-data";
import { isZooming } from "./zoom";


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
