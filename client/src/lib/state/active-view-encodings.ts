import type { Encodings } from '$lib/types/encodings';
import type { Writable } from 'svelte/store';
import { writable } from 'svelte/store';

export const activeViewEncodings: Writable<Encodings> = writable({
	x: null,
	y: null,
	color: null
});
