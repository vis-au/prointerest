import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type DataItem from '$lib/types/data-item';

export const interestingItems: Writable<DataItem[]> = writable([]);
