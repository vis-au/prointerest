import { writable } from 'svelte/store';

export const hoveredPosition = writable([-1, -1] as [number, number]);
