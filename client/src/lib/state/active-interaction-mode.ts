import type { InteractionMode } from "$lib/interaction/doi-interaction";
import { writable } from "svelte/store";

export const activeInteractionMode = writable("brush" as InteractionMode);