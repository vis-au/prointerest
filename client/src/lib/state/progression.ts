import type { ProgressionState } from "$lib/types/progression-state";
import { getNextChunk } from "$lib/util/requests";
import { writable } from "svelte/store";
import { processedData } from "./processed-data";
import { sendReset } from "../util/requests";

export const CHUNK_SIZE = 1000;

const currentInterval = 1000;
export const updateInterval = writable(currentInterval);

export const progressionState = writable("paused" as ProgressionState);

let currentlyWaiting = false;
export const waitingForChunk = writable(currentlyWaiting);

// function saveDoi(items: number[][], doi: number[]) {
//   activeDoiValues.update((dois) => {
//     items.forEach((item, i) => {
//       dois.set(item[0], doi[i]);
//     });

//     return dois;
//   });
// }

const progressionCallback = () => {
  if (!currentlyWaiting) {
    currentlyWaiting = true;
    waitingForChunk.set(true);
    getNextChunk(CHUNK_SIZE).then((chunk) => {
      processedData.update((processed) => {
        return [...processed, ...chunk.chunk];
      });
      currentlyWaiting = false;
      waitingForChunk.set(currentlyWaiting)
      // saveDoi(chunk.chunk, chunk.doi);
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
