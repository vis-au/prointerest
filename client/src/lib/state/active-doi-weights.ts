import type { PosteriorEntry, PriorEntry } from "$lib/types/doi-weights";
import type { InteractionMode } from "$lib/provenance/doi-interaction";
import { writable } from "svelte/store";
import { OutliernessMeasure, outliernessMeasures } from "$lib/types/outlier-measures";

const weights = new Map<"prior" | "posterior", number>();
weights.set("prior", 0.5);
weights.set("posterior", 0.5);
export const componentWeights = writable(weights);

const prior = new Map<PriorEntry, number>();
prior.set("dimensions", 0.3);
prior.set("outlierness", 0.7);
export const priorWeights = writable(prior);

const posterior = new Map<PosteriorEntry, number>();
posterior.set("provenance", 0.7);
posterior.set("scagnostics", 0.3);
export const posteriorWeights = writable(posterior);

const interactionTechniques = new Map<InteractionMode, number>();
interactionTechniques.set("scat-brush", 0.35);
interactionTechniques.set("hist-brush", 0.3);
interactionTechniques.set("select", 0.1);
interactionTechniques.set("inspect", 0.05);
interactionTechniques.set("zoom", 0.05);
export const interactionWeights = writable(interactionTechniques);

const currentOutliernessWeights = new Map<OutliernessMeasure, number>();
outliernessMeasures.forEach((measure) =>
  currentOutliernessWeights.set(measure, 1 / outliernessMeasures.length)
);
export const outliernessWeights = writable(currentOutliernessWeights);
