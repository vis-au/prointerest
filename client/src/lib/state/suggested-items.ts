import GuidanceProvider from '$lib/doi/guidance-provider';
import type DataItem from '$lib/types/data-item';
import type { SuggestionMode } from '$lib/types/indicate-mode';
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import { activeSuggestionMode } from './active-indicate-mode';
import { interestingItems } from './interesting-items';
import { quadtree } from './quadtree';
import { top100Ids } from './latest-doi-values';

const guide = new GuidanceProvider();

let currentlyInterestItems: DataItem[] = [];
let currentTop100Ids: number[];
let currentMode: SuggestionMode = null;

export const suggestedItems: Writable<DataItem[]> = writable([]);

function updateSuggestedItems() {
	if (currentMode === 'explored') {
		suggestedItems.set(currentlyInterestItems);
	} else if (currentMode === "interesting") {
		console.log(currentTop100Ids);
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

activeSuggestionMode.subscribe((newMode) => {
	currentMode = newMode;
	updateSuggestedItems();
});

quadtree.subscribe((newTree) => {
	guide.processedDataspace = newTree.data();
});

top100Ids.subscribe((items) => {
	currentTop100Ids = items;
	updateSuggestedItems();
});
