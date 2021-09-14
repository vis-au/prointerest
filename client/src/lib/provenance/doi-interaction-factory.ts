import type { Quadtree } from "d3-quadtree";
import type { ZoomTransform } from "d3-zoom";

import type DataItem from "../types/data-item";
import ScatterplotBrush from "./scatterplot-brush-interaction";
import Inspect from "./inspect-interaction";
import Select from "./select-interaction";
import ZoomAndPan from "./zoom-and-pan-interaction";

const STANDARD_DIVIATION = 20;

export default class InteractionFactory {
  private screenWidth: number;
  private screenHeight: number;
  private quadtree: Quadtree<DataItem>;
  private _getItemsInRegion: (x0: number, y0: number, x3: number, y3: number) => DataItem[];
  public getTimestamp: () => number;

  constructor(width: number, height: number, quadtree: Quadtree<DataItem>) {
    this.screenWidth = width;
    this.screenHeight = height;
    this.quadtree = quadtree;
    this._getItemsInRegion = () => [];
    this.getTimestamp = () => -1;
  }

  public createScatterplotBrushInteraction(
    x0: number,
    y0: number,
    x1: number,
    y1: number
  ): ScatterplotBrush {
    const brushInteraction = new ScatterplotBrush();

    brushInteraction.quadtree = this.quadtree;
    brushInteraction.getItemsInRegion = this._getItemsInRegion;
    brushInteraction.timestamp = this.getTimestamp();
    brushInteraction.x = x0;
    brushInteraction.width = Math.abs(x0 - x1);
    brushInteraction.y = y0;
    brushInteraction.height = Math.abs(y0 - y1);
    brushInteraction.std = STANDARD_DIVIATION;

    return brushInteraction;
  }

  public createZoomInteraction(transform: ZoomTransform): ZoomAndPan {
    const zoomInteraction = new ZoomAndPan();

    zoomInteraction.quadtree = this.quadtree;
    zoomInteraction.getItemsInRegion = this._getItemsInRegion;
    zoomInteraction.timestamp = this.getTimestamp();
    zoomInteraction.transform = transform;
    zoomInteraction.std = STANDARD_DIVIATION;
    zoomInteraction.width = this.screenWidth;
    zoomInteraction.height = this.screenHeight;

    return zoomInteraction;
  }

  public createInspectInteraction(x: number, y: number): Inspect {
    const inspectInteraction = new Inspect();

    inspectInteraction.quadtree = this.quadtree;
    inspectInteraction.getItemsInRegion = this._getItemsInRegion;
    inspectInteraction.timestamp = this.getTimestamp();
    inspectInteraction.x = x;
    inspectInteraction.y = y;
    inspectInteraction.std = STANDARD_DIVIATION;

    return inspectInteraction;
  }

  public createSelectInteraction(x: number, y: number): Select {
    const selectInteraction = new Select();

    selectInteraction.quadtree = this.quadtree;
    selectInteraction.getItemsInRegion = this._getItemsInRegion;
    selectInteraction.timestamp = this.getTimestamp();
    selectInteraction.x = x;
    selectInteraction.y = y;

    return selectInteraction;
  }

  public set width(w: number) {
    this.screenWidth = w;
  }

  public set height(h: number) {
    this.screenHeight = h;
  }

  public set getItemsInRegion(
    f: (x0: number, y0: number, x3: number, y3: number, t: Quadtree<DataItem>) => DataItem[]
  ) {
    this._getItemsInRegion = (_x0, _y0, _x3, _y3) => f(_x0, _y0, _x3, _y3, this.quadtree);
  }
}
