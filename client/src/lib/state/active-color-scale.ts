import { interpolateBuPu, scaleSequential, scaleSequentialLog } from 'd3';
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { ColorScaleType } from '$lib/types/color';

let currentScheme = interpolateBuPu;
export const colorScheme = writable(currentScheme);

let currentScaleType: ColorScaleType = 'linear';
export const colorScaleType: Writable<ColorScaleType> = writable(currentScaleType);

export const colorScale = writable(scaleSequential(currentScheme));

function updateScale() {
	const generator = currentScaleType === 'linear' ? scaleSequential : scaleSequentialLog;

	colorScale.set(generator(currentScaleType));
}

colorScheme.subscribe((newScheme) => {
	currentScheme = newScheme;
	updateScale();
});

colorScaleType.subscribe((type) => {
	currentScaleType = type;
	updateScale;
});
