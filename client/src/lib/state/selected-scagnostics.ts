import type { Scagnostic } from "$lib/types/scagnostics";
import { scagnostics } from "$lib/types/scagnostics";
import { writable } from "svelte/store";

export const selectedScagnostics = writable([] as Scagnostic[]);

const weights = new Map<Scagnostic, number>();
scagnostics.forEach(s => {
  weights.set(s, 1 / scagnostics.length);
});
export const scagnosticWeights = writable(weights);
