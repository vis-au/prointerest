import type DataItem from "$lib/types/data-item";
import type { Hexbin, HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";
import { hexbinning } from "./hexbinning";
import { visibleData } from "./visible-data";

export const bins = writable([] as HexbinBin<DataItem>[]);

let currentHexbinning = null as Hexbin<DataItem>;
let currentlyVisibleData = [] as DataItem[];

hexbinning.subscribe((h) => {
  currentHexbinning = h;
  bins.set(currentHexbinning(currentlyVisibleData));
});

visibleData.subscribe((data) => {
  currentlyVisibleData = data;
  bins.set(currentHexbinning(data));
});
