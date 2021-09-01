import type { InteractionMode } from '$lib/interaction/doi-interaction';
import { interactionModes } from '$lib/interaction/doi-interaction';
import { writable } from 'svelte/store';

const interactionTechniques = new Map<InteractionMode, number>();

interactionModes.forEach((mode) => {
	interactionTechniques.set(mode, 1 / interactionModes.length);
});

export const interactionWeights = writable(interactionTechniques);
