import type DataItem from "$lib/types/data-item";
import { writable } from "svelte/store";

export const selectionInSecondaryView = writable([] as DataItem[]);
