<script lang="ts">
  import { max, min } from "d3-array";
  import type { HexbinBin } from "d3-hexbin";
  import { scaleLog } from "d3-scale";
  import { afterUpdate, onMount } from "svelte";

  import { colorScale } from "$lib/state/active-color-scale";
  import {
    activeViewEncodings,
    getRGB,
    UNINTERESTING_COLOR
  } from "$lib/state/active-view-encodings";
  import { bins, uninterestingBins } from "$lib/state/bins";
  import { hexbinning } from "$lib/state/hexbinning";
  import type DataItem from "$lib/types/data-item";

  export let id = "binned-scatterplot-view";
  export let width = 100;
  export let height = 100;

  let updateInterval: number;
  let canvasElement: HTMLCanvasElement;
  let uninterestingCanvasElement: HTMLCanvasElement;

  const sizeScale = scaleLog();

  function renderBins(
    ctx: CanvasRenderingContext2D,
    hexagonPath: Path2D,
    renderInteresting: boolean
  ) {
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.strokeStyle = getRGB(UNINTERESTING_COLOR);
    ctx.lineWidth = 2;

    (renderInteresting ? $bins : $uninterestingBins).forEach((bin) => {
      ctx.translate(bin.x, bin.y);
      ctx.fillStyle = renderInteresting
        ? $colorScale($activeViewEncodings.color === "doi" ? bin["doi"] : bin.length)
        : getRGB(UNINTERESTING_COLOR);

      const scaleFactor = $activeViewEncodings.size === "count" ? sizeScale(bin.length) : 1;
      ctx.scale(scaleFactor, scaleFactor);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);

      ctx.translate(-bin.x, -bin.y);
      ctx.setTransform(1, 0, 0, 1, 0, 0); // reset the ctx transform
    });

    ctx.closePath();
  }

  function updateScales() {
    const minCount = min($bins, (d: HexbinBin<DataItem>) => d.length) || 0;
    const maxCount = max($bins, (d: HexbinBin<DataItem>) => d.length) || 1;

    if ($colorScale.range().length === 3) {
      $colorScale.domain(
        $activeViewEncodings.color === "doi" ? [-1, 0, 1] : [maxCount, 0, minCount]
      );
      sizeScale.domain($activeViewEncodings.size === "count" ? [minCount, maxCount] : [0, 1]);
    } else {
      $colorScale.domain($activeViewEncodings.color === "doi" ? [0, 1] : [minCount, maxCount]);
      sizeScale.domain($activeViewEncodings.size === "count" ? [minCount, maxCount] : [0, 1]);
    }
  }

  function render() {
    if (!canvasElement) {
      return;
    }

    const hexagonPath = new Path2D($hexbinning.hexagon());
    clearInterval(updateInterval);

    // update the color scale here, right before rendering the data
    updateScales();
    renderBins(canvasElement.getContext("2d"), hexagonPath, true);
    renderBins(uninterestingCanvasElement.getContext("2d"), hexagonPath, false);
  }

  afterUpdate(() => {
    updateInterval = setTimeout(render, 0) as unknown as number;
  });
  onMount(render);
</script>

<div id="{id}-binned-scatterplot-view" class="binned-scatterplot-view">
  <canvas
    id="{id}-uninteresting-bins-canvas"
    class="bins-canvas uninteresting"
    {width}
    {height}
    bind:this={uninterestingCanvasElement}
  />
  <canvas
    id="{id}-interesting-bins-canvas"
    class="bins-canvas"
    {width}
    {height}
    bind:this={canvasElement}
  />
</div>

<style>
  div.binned-scatterplot-view {
    position: relative;
  }
  div.binned-scatterplot-view canvas.bins-canvas {
    position: absolute;
  }
  div.binned-scatterplot-view canvas.bins-canvas.uninteresting {
    background: #efefef;
  }
</style>
