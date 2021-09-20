import type { ProgressionState } from "$lib/types/progression-state";
import { getNextChunk } from "$lib/util/requests";
import { writable } from "svelte/store";
import { processedData } from "./processed-data";
import { sendReset } from "../util/requests";
import { doiValues } from "./doi-values";
import { doiLabels } from "./doi-labels";

export const CHUNK_SIZE = 1000;

const currentInterval = 1000;
export const updateInterval = writable(currentInterval);

export const progressionState = writable("paused" as ProgressionState);

let currentlyWaiting = false;
export const waitingForChunk = writable(currentlyWaiting);

const currentDoiLabels: Map<number, number> = new Map();
const currentDoiValues: Map<number, number> = new Map();

const progressionCallback = () => {
  if (!currentlyWaiting) {
    currentlyWaiting = true;
    waitingForChunk.set(true);
    getNextChunk(CHUNK_SIZE).then((chunk) => {
      processedData.update((processed) => {
        return [...processed, ...chunk.chunk];
      });
      chunk.labels.forEach((label, i) => {
        currentDoiLabels.set(chunk.chunk[i][0], label);
      });
      chunk.dois.forEach((doi, i) => {
        currentDoiValues.set(chunk.chunk[i][0], doi);
      });

      doiLabels.update(() => currentDoiLabels);
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
  processedData.update(() => {
    return [];
  });
  sendReset();
}
