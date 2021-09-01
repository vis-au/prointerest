import { writable } from 'svelte/store';

export const activeBrush = writable([
	[null, null],
	[null, null]
] as [[number, number], [number, number]]);
