import type { BrushMode } from "$lib/types/brush-mode";
import { writable } from "svelte/store";

export const scatterplotBrush = writable("rect" as BrushMode);
