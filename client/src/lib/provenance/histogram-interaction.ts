import type DataItem from "../types/data-item";

export type HistogramInteractionMode = "hist-brush";
export const histogramInteractionModes: HistogramInteractionMode[] = ["hist-brush"];

export interface HistogramInteraction {
  mode: HistogramInteractionMode;
  dimension: string;
  index: number;
  extent: [number, number];
  std: number;
  timestamp: number;
  getAffectedItems: () => DataItem[];
}
