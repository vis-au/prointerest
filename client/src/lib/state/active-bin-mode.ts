import type { BinMode } from "$lib/types/bin-mode";
import { writable } from "svelte/store";

export const activeBinMode = writable("density" as BinMode)