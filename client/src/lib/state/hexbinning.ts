import { currentTransform } from '$lib/state/zoom';
import type DataItem from '$lib/types/data-item';
import type { ZoomTransform } from 'd3';
import { hexbin } from 'd3-hexbin';
import { writable } from 'svelte/store';

const currentHexBinning = hexbin<DataItem>().radius(10);
export const hexbinning = writable(currentHexBinning);

let transform: ZoomTransform;

currentTransform.subscribe((t) => {
	transform = t;
	currentHexBinning
		.x((d) => transform.applyX(d.position.x))
		.y((d) => transform.applyY(d.position.y));
	hexbinning.set(currentHexBinning);
});
