import { writable } from "svelte/store";
import type { Writable } from "svelte/store";
import type { SuggestionMode } from "$lib/types/suggestion-mode";

export const activeSuggestionMode: Writable<SuggestionMode> = writable("none");
