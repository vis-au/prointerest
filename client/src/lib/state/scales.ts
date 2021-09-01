import { scaleLinear } from 'd3-scale';
import { writable } from 'svelte/store';

export const scaleX = writable(scaleLinear());
export const scaleY = writable(scaleLinear());
