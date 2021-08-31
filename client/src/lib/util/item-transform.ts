export function arrayItemToRecord(arrayItem: number[]): Record<string, unknown> {
  const item = {};

  arrayItem.forEach((val, i) => {
    item[""+i] = val;
  });

  return item;
};