import type { Quadtree } from "d3-quadtree";
import type DataItem from "../types/data-item";

export type HistogramInteractionMode = "hist-brush";
export const histogramInteractionModes: HistogramInteractionMode[] = ["hist-brush"];

export interface HistogramInteraction {
  mode: HistogramInteractionMode;
  std: number;
  quadtree: Quadtree<DataItem>;
  timestamp: number;
  getAffectedItems: () => DataItem[];
}
