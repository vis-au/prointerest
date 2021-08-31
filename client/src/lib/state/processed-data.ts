import type { BinType } from "$lib/types/bin-type";
import { writable } from "svelte/store";

export const processedData = writable([] as BinType[]);

export const dimensions = writable([] as string[]);