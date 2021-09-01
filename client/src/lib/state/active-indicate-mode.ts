import { writable } from "svelte/store";
import type { Writable } from "svelte/store";
import type { IndicateMode } from "$lib/types/indicate-mode";

export const activeIndicateMode: Writable<IndicateMode> = writable("similar");