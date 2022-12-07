<script lang="ts">
  import { max, min } from "d3-array";
  import type { HexbinBin } from "d3-hexbin";
  import { afterUpdate, onMount } from "svelte";

  import type DataItem from "$lib/types/data-item";
  import { colorScale } from "$lib/state/active-color-scale";
  import { bins, uninterestingBins } from "$lib/state/bins";
  import { hexbinning } from "$lib/state/hexbinning";

  export let id = "binned-scatterplot-view";
  export let width = 100;
  export let height = 100;

  const UNINTERESTING_COLOR = "rgba(255, 255, 255, 0)";

  let updateInterval: number;
  let canvasElement: HTMLCanvasElement;
  let uninterestingCanvasElement: HTMLCanvasElement;

  function renderBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D, useInteresting: boolean) {
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.strokeStyle = "rgba(255,255,255,1)";
    ctx.lineWidth = 2;

    (useInteresting ? $bins : $uninterestingBins).forEach((bin) => {
      ctx.translate(bin.x, bin.y);
      ctx.fillStyle = useInteresting ? $colorScale(bin.length) : UNINTERESTING_COLOR;
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });

    ctx.closePath();
  }

  function updateColorScale() {
    const minCount = min($bins, (d: HexbinBin<DataItem>) => d.length) || 0;
    const maxCount = max($bins, (d: HexbinBin<DataItem>) => d.length) || 1;

    if ($colorScale.range().length === 3) {
      $colorScale.domain([maxCount, 0, minCount]);
    } else {
      $colorScale.domain([minCount, maxCount]);
    }
  }

  function render() {
    if (!canvasElement) {
      return;
    }

    const hexagonPath = new Path2D($hexbinning.hexagon());
    clearInterval(updateInterval);

    // update the color scale here, right before rendering the data
    updateColorScale();
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
