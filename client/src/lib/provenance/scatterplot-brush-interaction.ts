import type { Quadtree } from "d3-quadtree";
import type DataItem from "../types/data-item";
import type { ScatterplotInteraction, ScatterplotInteractionMode } from "./scatterplot-interaction";

export type ItemsInRegionCallback = (x0: number, y0: number, x3: number, y3: number) => DataItem[];

export default class ScatterplotBrush implements ScatterplotInteraction {
  public mode: ScatterplotInteractionMode = "scat-brush";
  public std = 0; // max distance from mean is 3*std
  public x = 0;
  public y = 0;
  public width = 0;
  public height = 0;
  public quadtree: Quadtree<DataItem> = null;
  public maxDistance = 0;
  public timestamp = -1;
  public getItemsInRegion: ItemsInRegionCallback = null;

  public getAffectedItems(): DataItem[] {
    if (this.getItemsInRegion === null) {
      return [];
    }

    const x0 = this.x - this.maxDistance;
    const x3 = this.x + this.width + this.maxDistance;
    const y0 = this.y - this.maxDistance;
    const y3 = this.y + this.height + this.maxDistance;

    const affectedDataItems = this.getItemsInRegion(x0, y0, x3, y3);

    return affectedDataItems;
  }
}
