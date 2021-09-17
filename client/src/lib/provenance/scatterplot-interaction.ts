import type { Quadtree } from "d3-quadtree";
import type DataItem from "../types/data-item";

export type ScatterplotInteractionMode = "scat-brush" | "inspect" | "zoom" | "select";
export const scatterplotInteractionModes: ScatterplotInteractionMode[] = [
  "scat-brush",
  "inspect",
  "zoom",
  "select"
];

export const defaultItemInRegion: (
  x0: number,
  y0: number,
  x3: number,
  y3: number
) => DataItem[] = () => [];

export interface ScatterplotInteraction {
  mode: ScatterplotInteractionMode;
  std: number;
  quadtree: Quadtree<DataItem>;
  timestamp: number;
  getAffectedItems: () => DataItem[];
}
