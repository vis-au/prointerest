import type { DoiEntry } from "$lib/types/doi-weights";
import { writable } from "svelte/store";

export const selectedDoiWeight = writable(null as DoiEntry);
