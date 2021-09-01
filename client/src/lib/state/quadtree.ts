import { quadtree as d3_quadtree } from 'd3-quadtree';
import type { ScaleLinear } from 'd3-scale';
import type DataItem from '$lib/types/data-item';
import { processedData } from './processed-data';
import { writable } from 'svelte/store';
import { xEncoding, yEncoding } from './visible-data';
import { scaleX, scaleY } from './scales';

const currentQuadtree = d3_quadtree<DataItem>()
	.x((d) => d.position.x)
	.y((d) => d.position.y);

export const quadtree = writable(currentQuadtree);

let currentScaleX: ScaleLinear<number, number> = null;
let currentScaleY: ScaleLinear<number, number> = null;
scaleX.subscribe((newScale) => (currentScaleX = newScale));
scaleY.subscribe((newScale) => (currentScaleY = newScale));

// is run asynchronously to ensure that the scales are set
setTimeout(() => {
	processedData.subscribe((newData) => {
		const newItems = newData.map((item) => {
			const newItem: DataItem = {
				id: Math.random(),
				position: {
					x: currentScaleX(item[xEncoding]),
					y: currentScaleY(item[yEncoding])
				},
				iteration: 0,
				values: item
			};

			return newItem;
		});

		currentQuadtree.addAll(newItems);
		quadtree.set(currentQuadtree);
	});
}, 0);
