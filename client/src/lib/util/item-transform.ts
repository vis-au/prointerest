import { doiValues } from "$lib/state/doi-values";
import { dimensions } from "$lib/state/processed-data";
import type DataItem from "$lib/types/data-item";

let currentDimensions: string[] = [];
dimensions.subscribe((dims) => (currentDimensions = dims));

let currentDoiValues: Map<number, number> = new Map();
doiValues.subscribe((values) => (currentDoiValues = values));

export function dataItemToRecord(dataItem: DataItem): Record<string, unknown> {
  const item = {};

  dataItem.values.forEach((val, i) => {
    item[currentDimensions[i]] = val;
  });

  item["selected"] = dataItem.selected;
  item["doi"] = currentDoiValues.get(dataItem.id);
  item["__item__"] = dataItem; // self reference

  return item;
}

export function dataItemToList(dataItem: DataItem): number[] {
  return dataItem.values;
}
