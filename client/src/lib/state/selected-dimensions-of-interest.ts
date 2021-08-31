import { writable } from "svelte/store";

export const selectedDimensionsOfInterest = writable([] as string[]);