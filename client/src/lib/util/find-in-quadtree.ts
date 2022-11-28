import type DataItem from "$lib/types/data-item";
import type { Quadtree, QuadtreeLeaf } from "d3-quadtree";
import { quadtree } from "$lib/state/quadtree";
import type { ScaleLinear } from "d3-scale";
import { scaleX, scaleY } from "$lib/state/scales";
import { sampledQuadtree } from "$lib/state/sampled-quadtree";
import { polygonContains } from "d3-polygon";

let currentQuadtree: Quadtree<DataItem>;
let currentSampledQuadtree: Quadtree<DataItem>;
let x: ScaleLinear<number, number>;
let y: ScaleLinear<number, number>;

// this is async to avoid error when loading page caused by access to lexical declaration of quadtr.
setTimeout(() => quadtree?.subscribe((newQuadtree) => (currentQuadtree = newQuadtree)), 0);
sampledQuadtree?.subscribe((t) => (currentSampledQuadtree = t));
scaleX.subscribe((s) => (x = s));
scaleY.subscribe((s) => (y = s));

// uses UNTRANSFORMED screen positions!
export function getPointsInR(x: number, y: number, r: number, tree = currentQuadtree): DataItem[] {
  if (tree === undefined) {
    return [];
  }

  const pointsInR: DataItem[] = [];
  const radius2 = r * r;

  tree.visit((node, x1, y1, x2, y2) => {
    if (node.length) {
      return x1 >= x + r || y1 >= y + r || x2 < x - r || y2 < y - r;
    }

    const d = (node as QuadtreeLeaf<DataItem>).data as DataItem;

    const dx = +d.position.x - x;
    const dy = +d.position.y - y;

    if (dx * dx + dy * dy < radius2) {
      pointsInR.push(d);
    }
  });

  return pointsInR;
}

// uses UNTRANSFORMED, BUT SCALED screen positions!
export function getPointsInRect(
  x0: number,
  y0: number,
  x3: number,
  y3: number,
  tree = currentQuadtree
): DataItem[] {
  if (tree === undefined) {
    return [];
  }

  const pointsInRect: DataItem[] = [];

  tree.visit((node, x1, y1, x2, y2) => {
    if (!node.length) {
      while (node !== undefined && node !== null) {
        const d = (node as QuadtreeLeaf<DataItem>).data as DataItem;
        const selected =
          d.position.x >= x0 && d.position.x < x3 && d.position.y >= y0 && d.position.y < y3;
        if (selected) {
          pointsInRect.push(d);
        }

        node = (node as QuadtreeLeaf<DataItem>).next;
      }

      return x1 >= x3 || y1 >= y3 || x2 < x0 || y2 < y0;
    }
  });

  return pointsInRect;
}

// uses UNTRANSFORMED, BUT SCALED screen positions!
export function getPointsInPolygon(
  polygon: [number, number][],
  tree = currentQuadtree
): DataItem[] {
  if (tree === undefined) {
    return [];
  }

  const items = tree.data();
  return items.filter((item) => {
    return polygonContains(polygon, [item.position.x, item.position.y]);
  });
}

// uses UNTRANSFORMED, UNSCALED DATA positions!
export function getUntransformedPointsInRect(
  x0: number,
  y0: number,
  x3: number,
  y3: number,
  tree = currentQuadtree
): DataItem[] {
  return getPointsInRect(x(x0), y(y0), x(x3), y(y3), tree);
}

// uses SCALED, BUT UNTRANSFORMED screen positions
export function getSampledPointsInRect(x0: number, y0: number, x3: number, y3: number): DataItem[] {
  return getPointsInRect(x0, y0, x3, y3, currentSampledQuadtree);
}
