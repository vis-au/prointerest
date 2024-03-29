import { mean } from "d3";
import { writable } from "svelte/store";

import type { ProgressionState } from "$lib/types/progression-state";
import { getNextChunk } from "$lib/util/requests";
import { sendReset } from "../util/requests";
import { activeBrush, activeLasso } from "./active-brush";
import { activeDecisionTree } from "./active-decision-tree";
import { averageDoiPerChunk, doiValues } from "./doi-values";
import { interestingIntervals } from "./interesting-dimensions";
import { processedData } from "./processed-data";
import { selectedDTNode } from "./selection-in-dt";
import { selectionInSecondaryView } from "./selection-in-secondary-view";
import { resetViewTransform } from "./zoom";

let currentChunkSize = 10000;
export const chunkSize = writable(currentChunkSize);
chunkSize.subscribe(($chunkSize) => (currentChunkSize = $chunkSize));

const currentInterval = 1000;
export const updateInterval = writable(currentInterval);

export const progressionState = writable("paused" as ProgressionState);

let currentlyWaiting = false;
export const waitingForChunk = writable(currentlyWaiting);

export const UPDATE_INTERVAL = 3; // fixed interval after which DOI values are recomputed
export const currentChunkNo = writable(0);

const currentDoiValues: Map<number, number> = new Map();

let isDoiFunctionCurrentlyDirty = false;
export const isDoiFunctionDirty = writable(isDoiFunctionCurrentlyDirty);
isDoiFunctionDirty.subscribe((flag) => (isDoiFunctionCurrentlyDirty = flag));


let currentlyUsingOurDoiApproach = true;
export const useOurDoiApproach = writable(currentlyUsingOurDoiApproach);
useOurDoiApproach.subscribe(flag => currentlyUsingOurDoiApproach = flag);


async function nextChunk() {
  const chunk = await getNextChunk(currentChunkSize, currentlyUsingOurDoiApproach);

  processedData.update((processed) => {
    return [...processed, ...chunk.chunk];
  });
  chunk.dois.forEach((doi, i) => {
    currentDoiValues.set(chunk.chunk[i][0], doi);
  });
  chunk.updated_dois.forEach((doi, i) => {
    const id = chunk.updated_dois[i];
    currentDoiValues.set(id, doi);
  });

  currentChunkNo.update((chunkNo) => {
    if (chunkNo > 0 && chunkNo % UPDATE_INTERVAL === 0) {
      // FIXME: triggers a full update of DOI values in a fixed interval. This should be replaced
      // by an on-demand approach, which updates only if the DOI values are outdated.
      isDoiFunctionDirty.set(true);
    }

    return chunkNo + 1;
  });

  averageDoiPerChunk.update((averageDois) => averageDois.concat(mean(chunk.dois)));
  doiValues.set(currentDoiValues);
}

const progressionCallback = async () => {
  if (!currentlyWaiting) {
    currentlyWaiting = true;
    waitingForChunk.set(true);

    if (isDoiFunctionCurrentlyDirty) {
      // TODO: do something to "clean" the DOI values
      isDoiFunctionDirty.set(false);
    } else {
      await nextChunk(); // side effect: sets isDoiFunctionDirty flag in reg. intervals
    }

    currentlyWaiting = false;
    waitingForChunk.set(currentlyWaiting);
  }
};

let progressionInterval: NodeJS.Timer = null;

export function startProgression(): void {
  progressionInterval = setInterval(progressionCallback, currentInterval);
  progressionState.set("running");
}

export function pauseProgression(): void {
  clearInterval(progressionInterval);
  progressionState.set("paused");
}

export function resetProgression(): void {
  pauseProgression();

  processedData.set([]);
  selectionInSecondaryView.set({});
  interestingIntervals.set({});
  currentChunkNo.set(0);
  activeBrush.set(null);
  activeLasso.set(null);
  selectedDTNode.set(null);
  selectionInSecondaryView.set({});
  currentDoiValues.clear();
  doiValues.set(currentDoiValues);
  activeDecisionTree.set(null);
  resetViewTransform();

  sendReset();
}
