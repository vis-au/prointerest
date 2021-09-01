import GuidanceProvider from '$lib/doi/guidance-provider';
import type DataItem from '$lib/types/data-item';
import type { IndicateMode } from '$lib/types/indicate-mode';
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import { activeIndicateMode } from './active-indicate-mode';
import { interestingItems } from './interesting-items';
import { quadtree } from './quadtree';

const guide = new GuidanceProvider();

let currentlyInterestItems: DataItem[] = [];
let currentMode: IndicateMode = null;

export const suggestedItems: Writable<DataItem[]> = writable([]);

function updateSuggestedItems() {
	if (currentMode === 'explored') {
		suggestedItems.set(currentlyInterestItems);
	} else if (currentMode === 'similar') {
		suggestedItems.set(guide.getItemsSimilarToInterest(currentlyInterestItems));
	} else if (currentMode === 'dissimilar') {
		suggestedItems.set(guide.getItemsDissimilarToInterest(currentlyInterestItems));
	}
}

interestingItems.subscribe((newItems) => {
	currentlyInterestItems = newItems;
	updateSuggestedItems();
});

activeIndicateMode.subscribe((newMode) => {
	currentMode = newMode;
	updateSuggestedItems();
});

quadtree.subscribe((newTree) => {
	guide.processedDataspace = newTree.data();
});
