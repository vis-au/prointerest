import { writable } from "svelte/store";
import { latestItems } from "./latest-chunk";
import { latestDoiUpdate } from "./latest-doi-update";
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

latestDoiUpdate.subscribe(($latestDoiUpdate) => {
  $latestDoiUpdate.ids.forEach((id) => {
    currentDoiTimestamps.set(+id, chunkNo);
  });

  doiTimestamps.set(currentDoiTimestamps);
});
