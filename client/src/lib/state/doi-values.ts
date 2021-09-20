import { writable } from "svelte/store";

export const doiValues = writable(new Map<number, number>());