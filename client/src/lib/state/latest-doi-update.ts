import type { DoiUpdate } from "$lib/types/doi-update";
import { writable } from "svelte/store";

export const latestDoiUpdate = writable(null as DoiUpdate);
