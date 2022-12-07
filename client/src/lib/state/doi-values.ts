import { writable } from "svelte/store";

export const doiValues = writable(new Map<number, number>());

export const averageDoiPerChunk = writable([] as number[]);
