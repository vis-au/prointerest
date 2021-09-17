import type DataItem from "$lib/types/data-item";
import type { Quadtree } from "d3-quadtree";
import type { ScatterplotInteraction, ScatterplotInteractionMode } from "./scatterplot-interaction";

export type ItemsInPolygonCallback = (polygon: [number, number][]) => DataItem[];

export default class ScatterplotLassoBrush implements ScatterplotInteraction {
  public mode: ScatterplotInteractionMode = "scat-brush";
  public std = 0;
  public polygon: [number, number][] = [];
  public quadtree: Quadtree<DataItem> = null;
  public timestamp = -1;
  public getItemsInRegion: ItemsInPolygonCallback = null;

  public getAffectedItems(): DataItem[] {
    const affectedItems = this.getItemsInRegion(this.polygon);
    return affectedItems;
  }
}