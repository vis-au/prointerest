import { derived } from "svelte/store";
import { hexbinning } from "./hexbinning";
import { randomDataSample } from "./sampled-data";
import { interestingItems, uninterestingItems } from "./items";
import { isZooming } from "./zoom";

export const bins = derived(
  [interestingItems, randomDataSample, hexbinning, isZooming],
  ([$interestingItems, $randomDataSample, $hexbinning, $isZooming]) => {
    return $hexbinning($isZooming ? $randomDataSample : $interestingItems);
  }
);

export const uninterestingBins = derived(
  [uninterestingItems, randomDataSample, hexbinning, isZooming],
  ([$uninterestingItems, $randomDataSample, $hexbinning, $isZooming]) => {
    return $hexbinning($isZooming ? $randomDataSample : $uninterestingItems);
  }
);
