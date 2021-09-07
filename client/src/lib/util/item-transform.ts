import type DataItem from "$lib/types/data-item";

export function dataItemToRecord(dataItem: DataItem): Record<string, unknown> {
  const item = {};

  dataItem.values.forEach((val, i) => {
    item["" + i] = val;
  });

  return item;
}

export function dataItemToList(dataItem: DataItem): number[] {
  return dataItem.values;
}
