import { dimensions } from "$lib/state/processed-data";
import type DataItem from "$lib/types/data-item";

let currentDimensions: string[] = [];
dimensions.subscribe(dims => currentDimensions = dims);

export function dataItemToRecord(dataItem: DataItem): Record<string, unknown> {
  const item = {};

  dataItem.values.forEach((val, i) => {
    item[currentDimensions[i]] = val;
  });

  return item;
}

export function dataItemToList(dataItem: DataItem): number[] {
  return dataItem.values;
}
