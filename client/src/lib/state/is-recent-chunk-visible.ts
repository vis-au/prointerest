import { writable } from "svelte/store";

export const isRecentChunkVisible = writable(true);

export const isOnlyInterestingRecentDataVisible = writable(true);
