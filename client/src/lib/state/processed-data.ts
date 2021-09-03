import { writable } from 'svelte/store';

export const processedData = writable([] as number[][]);

export const dimensions = writable([] as string[]);

export const totalSize = writable(-1);