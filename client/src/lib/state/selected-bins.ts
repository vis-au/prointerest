import type { HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import { currentTransform } from "./zoom";

export const selectedBins = writable([] as HexbinBin<DataItem>[]);

currentTransform.subscribe(() => selectedBins.set([]));
