import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { SuggestionMode } from '$lib/types/indicate-mode';

export const activeIndicateMode: Writable<SuggestionMode> = writable('similar');
