import type { HistogramInteractionMode, HistogramInteraction } from "./histogram-interaction";
import { histogramInteractionModes } from "./histogram-interaction";
import type { ScatterplotInteractionMode, ScatterplotInteraction } from "./scatterplot-interaction";
import { scatterplotInteractionModes } from "./scatterplot-interaction";

export type InteractionMode = HistogramInteractionMode | ScatterplotInteractionMode;
export const interactionModes: InteractionMode[] = [
  ...histogramInteractionModes,
  ...scatterplotInteractionModes
];

export const defaultDecay = (oldValue: number): number => 0.99 * oldValue;

export type DoiInteraction = ScatterplotInteraction | HistogramInteraction;
