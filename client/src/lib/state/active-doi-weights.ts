import type { PosteriorEntry, PriorEntry } from "$lib/types/doi-weights";
import { writable } from "svelte/store";

const prior = new Map<PriorEntry, number>();
prior.set("dimensions", 0.33)
prior.set("outlierness", 0.33);
prior.set("selection", 0.33);
export const priorWeights = writable(prior);

const posterior = new Map<PosteriorEntry, number>();
posterior.set("provenance", 0.5);
posterior.set("scagnostics", 0.5);
export const posteriorWeights = writable(posterior);