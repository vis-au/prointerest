import { quadtree as d3_quadtree } from 'd3-quadtree';
import type { ScaleLinear } from 'd3-scale';
import type DataItem from '$lib/types/data-item';
import { processedData } from './processed-data';
import { writable } from 'svelte/store';
import { scaleX, scaleY } from './scales';
import { activeViewEncodings } from './active-view-encodings';
import { dimensions } from './processed-data';
import { resetProgression } from './progression';

let currentQuadtree = createQuadtree();
export const quadtree = writable(currentQuadtree);

let currentScaleX: ScaleLinear<number, number> = null;
let currentScaleY: ScaleLinear<number, number> = null;

let currentDimensions: string[] = [];
let xIndex = -1;
let yIndex = -1;


function createQuadtree() {
	return d3_quadtree<DataItem>()
		.x((d) => d.position.x)
		.y((d) => d.position.y);
}

function arrayToDataItem(item: number[]) {
	const newItem: DataItem = {
		id: Math.random(),
		position: {
			x: currentScaleX(item[xIndex]),
			y: currentScaleY(item[yIndex])
		},
		iteration: 0,
		values: item
	};

	return newItem;
}

// is run asynchronously to ensure that the scales are set
setTimeout(() => {
	processedData.subscribe((newData) => {
		const newItems = newData.map(arrayToDataItem);

		if (newData.length === 0) {
			// in case the progression was reset, clear the quadtree as well.
			currentQuadtree = createQuadtree();
		} else {
			// otherwise just add the data to the quadtree
			currentQuadtree.addAll(newItems);
		}

		quadtree.set(currentQuadtree);
	});
}, 0);

scaleX.subscribe((newScale) => currentScaleX = newScale);
scaleY.subscribe((newScale) => currentScaleY = newScale);

dimensions.subscribe(newDims => currentDimensions = newDims);

activeViewEncodings.subscribe(newEncodings => {
	xIndex = currentDimensions.indexOf(newEncodings.x);
	yIndex = currentDimensions.indexOf(newEncodings.y);
	resetProgression();
});