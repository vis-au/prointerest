import { linear } from "$lib/types/doi-interpolation-function";
import { writable } from "svelte/store";

export const selectedDoiInterpolationFunction = writable(linear);