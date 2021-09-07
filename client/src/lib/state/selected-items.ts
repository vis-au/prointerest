import type { HexbinBin } from 'd3-hexbin';
import { writable } from 'svelte/store';

import type DataItem from '$lib/types/data-item';
import { getPointsInR, getPointsInRect } from '$lib/util/find-in-quadtree';
import { activeBrush } from './active-brush';
import { quadtree } from './quadtree';
import { selectedBins } from './selected-bins';

export const selectedItems = writable([] as DataItem[]);

let currentSelectedBins: HexbinBin<DataItem>[] = [];
let currentBrush: [[number, number], [number, number]] = [
	[-1, -1],
	[-1, -1]
];

function getBrushedItems() {
	if (currentBrush === null || currentBrush[0] === null) {
		return [];
	}

	const [[x0, y0], [x1, y1]] = currentBrush;
	return getPointsInRect(x0, y0, x1, y1);
}

function getItemsInSelectedBins() {
	return currentSelectedBins.map((bin) => getPointsInR(bin.x, bin.y, 10)).flat();
}

function getSelectedItems() {
	const brushedItems = getBrushedItems();
	const itemsInBins = getItemsInSelectedBins();

	return brushedItems.concat(itemsInBins);
}

quadtree.subscribe(() => {
	selectedItems.set(getSelectedItems());
});

activeBrush.subscribe((newBrush) => {
	currentBrush = newBrush;
	selectedItems.set(getSelectedItems());
});

selectedBins.subscribe((newBins) => {
	currentSelectedBins = newBins;
	selectedItems.set(getSelectedItems());
});
