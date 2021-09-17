import { writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";


export const exploredItems = writable([] as DataItem[]);
export const exploredItemInterest = writable(new Map<DataItem, number>());
