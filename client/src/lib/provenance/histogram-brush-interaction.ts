import type DataItem from "$lib/types/data-item";
import type { HistogramInteraction, HistogramInteractionMode } from "./histogram-interaction";

export default class HistogramBrush implements HistogramInteraction {
  public mode: HistogramInteractionMode = "hist-brush";
  public std: number = null;
  public dimension: string = null; // dimension used for binning
  public index: number; // dimension's index in list of all dimensions
  public extent: [number, number] = null;
  public data: DataItem[];
  public timestamp: number = null;

  public getAffectedItems(): DataItem[] {
    return this.data.filter(
      (item) => item.values[this.index] > this.extent[0] && item.values[this.index] < this.extent[1]
    );
  }
}
