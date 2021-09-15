<script lang="typescript">
  import { geoPath } from "d3-geo";
  import type { GeoPermissibleObjects } from "d3-geo";
  import type { ZoomTransform } from "d3-zoom";
  import { afterUpdate } from "svelte";

  import { activeBrush, activeLasso } from "$lib/state/active-brush";
  import { scatterplotBrush } from "$lib/state/active-scatterplot-brush";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { selectedItems } from "$lib/state/selected-items";
  import { currentTransform } from "$lib/state/zoom";
  import { separateThousands } from "$lib/util/number-transform";

  export let width: number;
  export let height: number;

  let canvas: HTMLCanvasElement;

  afterUpdate(render);

  function renderBrush(ctx: CanvasRenderingContext2D, t: ZoomTransform) {
    if ($scatterplotBrush !== "rect" || !$activeBrush) {
      return;
    }

    const [[_x0, _y0], [_x1, _y1]] = $activeBrush;
    const x0 = t.applyX($scaleX(_x0));
    const y0 = t.applyY($scaleY(_y0));
    const x1 = t.applyX($scaleX(_x1));
    const y1 = t.applyY($scaleY(_y1));

    // draw brush
    ctx.rect(x0, y0, Math.abs(x0 - x1), Math.abs(y0 - y1));
    ctx.stroke();

    // draw label
    ctx.font = "13px sans-serif";
    ctx.fillText(`${separateThousands($selectedItems.length)} points`, x0, y1 + 15);
  }

  function renderLasso(ctx: CanvasRenderingContext2D, t: ZoomTransform) {
    if ($scatterplotBrush !== "lasso" || !$activeLasso) {
      return;
    }

    const coordinates = $activeLasso.map((p) => [t.applyX($scaleX(p[0])), t.applyY($scaleY(p[1]))]);

    const path = geoPath().context(ctx);
    const pathObj = { type: "LineString", coordinates };
    path(pathObj as GeoPermissibleObjects); // draws the polygon onto the canvas
    ctx.lineWidth = 2;
    ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
    ctx.fill();

    // draw label
    const first = coordinates[0];
    ctx.font = "13px sans-serif";
    ctx.fillStyle = "rgba(0, 0, 0, 1)";
    ctx.fillText(`${separateThousands($selectedItems.length)} points`, first[0] + 15, first[1]);
    ctx.stroke();
  }

  function render() {
    const ctx = canvas.getContext("2d");
    const t = $currentTransform;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.strokeStyle = "rgba(0,0,0,0.73)";

    renderBrush(ctx, t);
    renderLasso(ctx, t);

    ctx.closePath();
  }
</script>

<canvas id="active-brush-layer" {width} {height} bind:this={canvas} />

<style>
  canvas#active-brush-layer {
    position: absolute;
  }
</style>
