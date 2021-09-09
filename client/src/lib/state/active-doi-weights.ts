import type { PosteriorEntry, PriorEntry } from "$lib/types/doi-weights";
import { writable } from "svelte/store";

const weights = new Map<"prior"|"posterior", number>();
weights.set("prior", 0.5);
weights.set("posterior", 0.5);
export const componentWeights = writable(weights);

const prior = new Map<PriorEntry, number>();
prior.set("dimensions", 0.15);
prior.set("outlierness", 0.7);
prior.set("selection", 0.15);
export const priorWeights = writable(prior);

const posterior = new Map<PosteriorEntry, number>();
posterior.set("provenance", 0.7);
posterior.set("scagnostics", 0.3);
export const posteriorWeights = writable(posterior);
