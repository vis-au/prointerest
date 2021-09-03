import type { ProgressionState } from "$lib/types/progression-state";
import { getNextChunk } from "$lib/util/requests";
import { writable } from "svelte/store";
import { processedData } from "./processed-data";

const currentInterval = 1000;
export const updateInterval = writable(currentInterval);

export const progressionState = writable("paused" as ProgressionState);

const progressionCallback = () => {
  getNextChunk().then(chunk => {
    processedData.update(processed => {
      return [...processed, ...chunk];
    });
  });
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
  progressionState.set("paused");
  processedData.update(() => {
    return [];
  });
}