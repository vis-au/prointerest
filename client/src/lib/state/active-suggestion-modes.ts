import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { SuggestionInput, SuggestionOutput } from '$lib/types/suggestion-mode';

export const activeSuggestionInput: Writable<SuggestionInput> = writable('interesting');
export const activeSuggestionOutput: Writable<SuggestionOutput> = writable('similar');
