import type { InteractionMode } from "$lib/provenance/doi-interaction";
import { writable } from "svelte/store";

export const activeInteractionMode = writable("zoom" as InteractionMode);
