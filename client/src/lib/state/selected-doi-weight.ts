import { writable } from "svelte/store";
import type { DOIDimension } from "$lib/types/doi-dimension";

export const selectedDoiWeight = writable(null as DOIDimension);
