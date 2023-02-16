import { bin, range } from "d3";
import { derived, writable } from "svelte/store";
import { latestItems } from "./latest-chunk";
import { currentChunkNo } from "./progression";

const currentDoiTimestamps = new Map<number, number>();
export const doiTimestamps = writable(currentDoiTimestamps);

let chunkNo = -1;
currentChunkNo.subscribe(($currentChunkNo) => (chunkNo = $currentChunkNo));

latestItems.subscribe(($latestItems) => {
  $latestItems.forEach((item) => {
    currentDoiTimestamps.set(item.id, chunkNo);
  });

  doiTimestamps.set(currentDoiTimestamps);
});

export const doiAgeHistogram = derived([doiTimestamps], ([$doiTimestamps]) => {
  if (doiTimestamps === null) {
    return [];
  }

  const timestamps = Array.from($doiTimestamps.values());
  const binGenerator = bin().thresholds(range(0, chunkNo, 1));
  const bins = binGenerator(timestamps);

  return bins;
});
