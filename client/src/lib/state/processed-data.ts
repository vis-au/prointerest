import type { DOIDimension } from "$lib/types/doi-dimension";
import { writable } from "svelte/store";

export const processedData = writable([] as number[][]);

export const dimensions = writable([] as DOIDimension[]);

export const totalSize = writable(-1);
