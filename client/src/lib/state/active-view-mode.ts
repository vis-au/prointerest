import type { ViewMode } from "$lib/types/view-modes";
import { writable } from "svelte/store";

export const activeViewMode = writable("binned" as ViewMode);