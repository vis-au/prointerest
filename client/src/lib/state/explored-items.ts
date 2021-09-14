import { readable, writable } from "svelte/store";
import type DataItem from "$lib/types/data-item";
import InteractionObserver from "$lib/provenance/interaction-observer";
import { getPointsInR } from "$lib/util/find-in-quadtree";
import type { DoiInteraction } from "$lib/provenance/doi-interaction";
import { sendInterestingItems } from "$lib/util/requests";
import type { InteractionLog } from "$lib/provenance/interaction-log";
import { interactionWeights } from "./interaction-technique-weights";
import { lessRandomlySampledItems } from "./randomly-sampled-items";

export const interactionObserver = new InteractionObserver(getPointsInR);

let currentInteractedThreshold = 0.25;
export const interactionThreshold = writable(currentInteractedThreshold);
let currentProvenanceLogSize = 100;
export const provenanceLogSize = writable(currentProvenanceLogSize);

export const exploredItems = writable([] as DataItem[]);
export const exploredItemInterest = writable(new Map<DataItem, number>());
export const provenanceLog = readable(interactionObserver.interactionLog as InteractionLog);

export function registerNewInteraction(interaction: DoiInteraction): void {
  interactionObserver.interactionLog.add(interaction);
}

export function getLatestTimestamp(): number {
  return interactionObserver.interactionLog.getLatestTimestamp();
}

export function updateExploredItems(): void {
  setTimeout(() => {
    interactionObserver.interestThreshold = currentInteractedThreshold;
    interactionObserver.recentSteps = currentProvenanceLogSize;

    const explored = interactionObserver.getExploredData();
    exploredItemInterest.set(explored);

    const items = Array.from(explored.keys());
    const values = Array.from(explored.values());
    exploredItems.set(items);

    sendInterestingItems(
      items.map((d) => d.id + ""),
      values
    );

    return items;
  }, 0);
}

interactionWeights.subscribe((weights) => {
  interactionObserver.doiWeights = weights;
});

interactionThreshold.subscribe((threshold) => {
  currentInteractedThreshold = threshold;
  updateExploredItems();
});

provenanceLogSize.subscribe((size) => {
  currentProvenanceLogSize = size;
  updateExploredItems();
});

lessRandomlySampledItems.subscribe((items) => {
  console.log("asdf", items);
  interactionObserver.data = items.slice(0);
});
