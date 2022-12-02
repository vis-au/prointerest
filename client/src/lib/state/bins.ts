import { derived } from "svelte/store";
import { hexbinning } from "./hexbinning";
import { randomDataSample } from "./sampled-data";
import { visibleInterestingData } from "./visible-data";
import { isZooming } from "./zoom";

export const bins = derived(
  [visibleInterestingData, randomDataSample, hexbinning, isZooming],
  ([$visibleInterestingData, $randomDataSample, $hexbinning, $isZooming]) => {
    return $hexbinning($isZooming ? $randomDataSample : $visibleInterestingData);
  }
);
