import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type DataItem from '$lib/types/data-item';
import InterestWatchDog from '$lib/doi/interest-watchdog';
import { getPointsInR } from '$lib/util/find-in-quadtree';
import { quadtree } from './quadtree';
import type { DoiInteraction } from '$lib/interaction/doi-interaction';
import { sendInterestingItems } from '$lib/util/requests';

export const interestingItems: Writable<DataItem[]> = writable([]);

const doiWatchdog = new InterestWatchDog(getPointsInR);

export function registerNewInteraction(interaction: DoiInteraction): void {
	doiWatchdog.interactionLog.add(interaction);
}

export function updateInterestingItems(): void {
	const interesting = doiWatchdog.getDataOfInterest();
	const items = Array.from(interesting.keys());
	const values = Array.from(interesting.values());
	interestingItems.set(items);
	sendInterestingItems(
		items.map((d) => d.id + ''),
		values
	);
}

export function getLatestTimestamp(): number {
	return doiWatchdog.interactionLog.getLatestTimestamp();
}

quadtree.subscribe((newTree) => {
	doiWatchdog.processedDataspace = newTree.data();
});
