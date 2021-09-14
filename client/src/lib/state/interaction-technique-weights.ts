import type { InteractionMode } from "$lib/provenance/doi-interaction";
import { writable } from "svelte/store";

const interactionTechniques = new Map<InteractionMode, number>();
interactionTechniques.set("scat-brush", 0.35);
interactionTechniques.set("hist-brush", 0.3);
interactionTechniques.set("select", 0.1);
interactionTechniques.set("inspect", 0.05);
interactionTechniques.set("zoom", 0.05);

export const interactionWeights = writable(interactionTechniques);
