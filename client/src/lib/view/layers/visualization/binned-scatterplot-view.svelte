<script lang="typescript">
  import { max, min } from "d3-array";
  import type { HexbinBin } from "d3-hexbin";
  import { afterUpdate, onMount } from "svelte";

  import type DataItem from "$lib/types/data-item";
  import { activeBinMode } from "$lib/state/active-bin-mode";
  import { colorScale } from "$lib/state/active-color-scale";
  import { bins } from "$lib/state/bins";
  import { doiValues } from "$lib/state/doi-values";
  import { hexbinning } from "$lib/state/hexbinning";

  export let id = "binned-scatterplot-view";
  export let width = 100;
  export let height = 100;

  let updateInterval: number;
  let canvasElement: HTMLCanvasElement;

  function getBinValue(bin: HexbinBin<DataItem>) {
    if ($activeBinMode === "density") {
      return bin.length;
    } else {
      return bin
        .map(item => +$doiValues.get(item.id))
        .reduce((a: number, b: number) => a + b, 0);
    }
  }

  function renderBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    clearInterval(updateInterval);
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.strokeStyle = "rgba(255,255,255,1)";
    ctx.lineWidth = 2;
    $bins.forEach((bin) => {
      ctx.translate(bin.x, bin.y);
      ctx.fillStyle = $colorScale(getBinValue(bin));
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
  }

  function updateColorScale() {
    const minCount = min($bins, (d: HexbinBin<DataItem>) => getBinValue(d)) || 0;
    const maxCount = max($bins, (d: HexbinBin<DataItem>) => getBinValue(d)) || 1;

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

    const ctx = canvasElement.getContext("2d");
    const hexagonPath = new Path2D($hexbinning.hexagon());

    // update the color scale here, right before rendering the data
    updateColorScale();
    renderBins(ctx, hexagonPath);
  }

  afterUpdate(() => {
    updateInterval = (setTimeout(render, 0) as unknown) as number;
  });
  onMount(render);
</script>

<div id="{id}-binned-scatterplot-view" class="binned-scatterplot-view">
  <canvas id="{id}-bins-canvas" class="bins-canvas" {width} {height} bind:this={canvasElement} />
</div>

<style>
  div.binned-scatterplot-view {
    position: relative;
  }
  div.binned-scatterplot-view canvas.bins-canvas {
    position: absolute;
    background: #efefef;
  }
</style>
