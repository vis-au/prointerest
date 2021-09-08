import type DataItem from "$lib/types/data-item";
import { writable } from "svelte/store";

export const interestingItems = writable([] as DataItem[]);