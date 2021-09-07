import { writable } from 'svelte/store';

export const activeDoiValues = writable(new Map<number, number>()); // id -> doi from server
export const top100Ids = writable([] as number[]); // list of ids

activeDoiValues.subscribe((values) => {
	const ids: [number, number][] = []; // id, interest
	values.forEach((value, key) => {
		ids.push([key, value]);
	});
	ids.sort((a, b) => b[1] - a[1]); // top first
	const top100 = ids.slice(0, 100).map((pair) => pair[0]);

	top100Ids.set(top100);
});
