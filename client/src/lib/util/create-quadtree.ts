import type { Quadtree } from "d3-quadtree";
import { quadtree as d3_quadtree } from "d3-quadtree";
import type DataItem from "$lib/types/data-item";

export function createQuadtree(): Quadtree<DataItem> {
  return d3_quadtree<DataItem>()
    .x((d) => d.position.x)
    .y((d) => d.position.y);
}
