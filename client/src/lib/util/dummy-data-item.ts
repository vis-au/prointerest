import { dimensions } from "$lib/state/processed-data";
import type DataItem from "$lib/types/data-item";

let currentDimensions = ["a", "b"];

export function getDummyDataItem(): DataItem {
  return {
    id: -1,
    position: { x: -1, y: -1 },
    iteration: -1,
    values: currentDimensions.map(() => null)
  };
}

dimensions.subscribe((dims) => currentDimensions = dims);