import { writable } from "svelte/store";
import type { Writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import InteractionObserver from "$lib/provenance/interaction-observer";
import { getPointsInR } from "$lib/util/find-in-quadtree";
import { quadtree } from "./quadtree";
import type { DoiInteraction } from "$lib/provenance/doi-interaction";
import { sendInterestingItems } from "$lib/util/requests";

export const exploredItems: Writable<DataItem[]> = writable([]);

const interactionObserver = new InteractionObserver(getPointsInR);

export function registerNewInteraction(interaction: DoiInteraction): void {
  interactionObserver.interactionLog.add(interaction);
}

export function getLatestTimestamp(): number {
  return interactionObserver.interactionLog.getLatestTimestamp();
}

export function updateExploredItems(): void {
  const explored = interactionObserver.getExploredData();
  const items = Array.from(explored.keys());
  const values = Array.from(explored.values());

  exploredItems.set(items);

  sendInterestingItems(
    items.map((d) => d.id + ""),
    values
  );
}

quadtree.subscribe((newTree) => {
  interactionObserver.processedDataspace = newTree.data();
});
