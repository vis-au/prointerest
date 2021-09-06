import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { SuggestionMode } from '$lib/types/indicate-mode';

export const activeSuggestionMode: Writable<SuggestionMode> = writable('similar');
