import { quadtree as d3_quadtree} from "d3-quadtree";
import type { Quadtree } from "d3-quadtree";
import type DataItem from "../types/data-item";
import type { DoiInteraction, InteractionMode } from "./doi-interaction";

export default class Inspect implements DoiInteraction {
  public mode: InteractionMode = "inspect";
  public std = 0;
  public x = 0;
  public y = 0;
  public quadtree: Quadtree<DataItem> = d3_quadtree<DataItem>();
  public timestamp = -1;
  public getItemsInRegion = (x0: number, y0: number, x3: number, y3: number): DataItem[] => [];

  private distance2D(x0: number, y0: number, x1: number, y1: number) {
    return Math.sqrt((x0 - x1)**2 + (y0 - y1)**2);
  }

  public getAffectedItems(): DataItem[] {
    const x0 = this.x - this.std*2;
    const x3 = this.x + this.std*2;
    const y0 = this.y - this.std*2;
    const y3 = this.y + this.std*2;
    const r = this.std;

    const affectedDataItems = this.getItemsInRegion(x0, y0, x3, y3)
      .filter(item => {
        const distance = this.distance2D(this.x, this.y, item.position.x, item.position.y);
        const inRange = distance < r;

        return inRange;
      });

    return affectedDataItems;
  }
}