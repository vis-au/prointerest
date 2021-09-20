import { writable } from "svelte/store";

export const doiLabels = writable(new Map<number, number>());