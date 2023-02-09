<script lang="ts">
  import { afterUpdate } from "svelte";

  import { colorArrayToRGB, PRIMARY_COLOR } from "$lib/state/active-view-encodings";
  import { hexbinning } from "$lib/state/hexbinning";
  import { latestBins, latestInterestingBins, latestItems, latestInterestingItems } from "$lib/state/latest-chunk";
  import { currentTransform } from "$lib/state/zoom";
    import { isOnlyInterestingRecentDataVisible } from "$lib/state/is-recent-chunk-visible";

  export let width: number;
  export let height: number;
  export let color = colorArrayToRGB(PRIMARY_COLOR); // black color of points
  export let radius = 3; // size of points
  export let useBinning = true;

  let canvasElement: HTMLCanvasElement = null;
  let offCanvas: HTMLCanvasElement = null;

  const opacity = 0.3;
  const lineWidth = 1;
  $: pointSize = radius * 2 + lineWidth * 2;

  $: items = $isOnlyInterestingRecentDataVisible ? $latestInterestingItems : $latestItems;
  $: bins = $isOnlyInterestingRecentDataVisible ? $latestInterestingBins : $latestBins;

  // https://stackoverflow.com/a/13916313
  function renderPoints() {
    const ctx = canvasElement.getContext("2d");
    ctx.clearRect(0, 0, width, height);

    const offCtx = offCanvas.getContext("2d");
    offCtx.clearRect(0, 0, pointSize, pointSize);
    offCtx.fillStyle = "transparent";
    offCtx.strokeStyle = color;
    offCtx.lineWidth = lineWidth;

    // draw the circle once ...
    offCtx.beginPath();
    offCtx.arc(pointSize / 2, pointSize / 2, radius, 0, 2 * Math.PI);
    offCtx.globalAlpha = opacity;
    offCtx.closePath();
    offCtx.fill();
    offCtx.stroke();

    const t = $currentTransform;

    const positions = items.map((item) => {
      return t.apply([item.position.x, item.position.y]);
    });

    // ... and then copy-paste it for every recent point in the dataset
    positions.forEach((position) => {
      ctx.drawImage(offCanvas, position[0] - radius, position[1] - radius, pointSize, pointSize);
    });
  }

  function renderBins() {
    const ctx = canvasElement.getContext("2d");
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "rgba(255,255,255,0)";
    ctx.strokeStyle = color;
    ctx.lineWidth = 1;
    ctx.beginPath();

    const hexagonPath = new Path2D($hexbinning.hexagon());

    bins.forEach((bin) => {
      ctx.translate(bin.x, bin.y);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);

      ctx.translate(-bin.x, -bin.y);
      ctx.setTransform(1, 0, 0, 1, 0, 0); // reset the ctx transform
    });

    ctx.closePath();
  }

  function render() {
    if (useBinning) {
      renderBins();
    } else {
      renderPoints();
    }
  }

  afterUpdate(render);
</script>

<div id="recent-points" class="recent-points">
  <canvas
    id="recent-points-canvas"
    class="recent-points-canvas"
    {width}
    {height}
    bind:this={canvasElement}
  />
  <canvas class="off" width={pointSize} height={pointSize} bind:this={offCanvas} />
</div>

<style>
  div.recent-points {
    position: relative;
  }
  canvas.recent-points-canvas,
  canvas.off {
    position: absolute;
  }
  canvas.off {
    display: none;
  }
</style>
