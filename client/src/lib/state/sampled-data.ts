import { derived, writable } from "svelte/store";
import { sample } from "../util/sample";
import { interestingItems } from "./items";



let currentSampleSize = 5000;
export const sampleSize = writable(currentSampleSize);
sampleSize.subscribe(newSize => currentSampleSize = newSize);


export const randomDataSample = derived([interestingItems], ([$interestingItems]) => {
  const sampleProbability = currentSampleSize / $interestingItems.length;
  return $interestingItems.filter(() => sample(sampleProbability));
});