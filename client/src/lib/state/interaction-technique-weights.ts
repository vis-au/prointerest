import type { InteractionMode } from "$lib/provenance/doi-interaction";
import { writable } from "svelte/store";

const interactionTechniques = new Map<InteractionMode, number>();
interactionTechniques.set("brush", 0.75);
interactionTechniques.set("select", 0.1);
interactionTechniques.set("inspect", 0.1);
interactionTechniques.set("zoom", 0.0);

export const interactionWeights = writable(interactionTechniques);
