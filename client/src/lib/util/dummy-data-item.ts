import type DataItem from "$lib/types/data-item";

export function getDummyDataItem(): DataItem {
  return {
    id: -1,
    position: { x: -1, y: -1 },
    iteration: -1,
    values: [-1, -1]
  };
}