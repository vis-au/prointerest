import { mean } from "d3";
import { writable } from "svelte/store";

import type { ProgressionState } from "$lib/types/progression-state";
import { getNextChunk } from "$lib/util/requests";
import { processedData } from "./processed-data";
import { sendReset } from "../util/requests";
import { averageDoiPerChunk, doiValues } from "./doi-values";
import { selectionInSecondaryView } from "./selection-in-secondary-view";
import { interestingIntervals } from "./interesting-dimensions";
import { activeDecisionTree } from "./active-decision-tree";

export const CHUNK_SIZE = 10000;

const currentInterval = 1000;
export const updateInterval = writable(currentInterval);

export const progressionState = writable("paused" as ProgressionState);

let currentlyWaiting = false;
export const waitingForChunk = writable(currentlyWaiting);

export const currentChunkNo = writable(0);

const currentDoiValues: Map<number, number> = new Map();

const progressionCallback = () => {
  if (!currentlyWaiting) {
    currentlyWaiting = true;
    waitingForChunk.set(true);
    getNextChunk(CHUNK_SIZE).then((chunk) => {
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

      currentChunkNo.update((chunkNo) => chunkNo + 1);
      averageDoiPerChunk.update((averageDois) => averageDois.concat(mean(chunk.dois)));
      doiValues.update(() => currentDoiValues);

      currentlyWaiting = false;
      waitingForChunk.set(currentlyWaiting);
    });
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
  currentDoiValues.clear();
  doiValues.set(currentDoiValues);
  activeDecisionTree.set(null);

  sendReset();
}
