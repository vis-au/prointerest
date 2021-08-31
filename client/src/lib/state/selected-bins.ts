import type { BinType } from "$lib/types/bin-type";
import type { HexbinBin } from "d3-hexbin";
import { writable } from "svelte/store";
import { currentTransform } from "./zoom";

export const selectedBins = writable([] as HexbinBin<BinType>[]);

currentTransform.subscribe(() => selectedBins.set([]));