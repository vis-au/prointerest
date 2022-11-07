import type DataItem from "$lib/types/data-item";
import type { Hexbin, HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";
import { hexbinning } from "./hexbinning";
import { interestingData } from "./visible-data";

export const bins = writable([] as HexbinBin<DataItem>[]);

let currentHexbinning = null as Hexbin<DataItem>;
let currentlyVisibleData = [] as DataItem[];

function updateBins() {
  bins.set(currentHexbinning(currentlyVisibleData));
}

hexbinning.subscribe((h) => {
  currentHexbinning = h;
  updateBins();
});

interestingData.subscribe((data) => {
  currentlyVisibleData = data;
  updateBins();
});
