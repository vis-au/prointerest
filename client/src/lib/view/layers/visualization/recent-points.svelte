<script lang="ts">
  import { afterUpdate } from "svelte";
  import { currentTransform } from "$lib/state/zoom";
  import { latestInterestingItems } from "$lib/state/latest-chunk";

  export let width: number;
  export let height: number;
  export let color = "rgba(0, 0, 0, 1)"; // black color of points
  export let radius = 1.5; // size of points

  let canvasElement: HTMLCanvasElement = null;
  let offCanvas: HTMLCanvasElement = null;

  const opacity = 0.3;
  const lineWidth = 0;
  $: pointSize = radius * 2 + lineWidth * 2;

  // https://stackoverflow.com/a/13916313
  function render() {
    const ctx = canvasElement.getContext("2d");
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = color;
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;

    const offCtx = offCanvas.getContext("2d");
    offCtx.clearRect(0, 0, pointSize, pointSize);
    offCtx.fillStyle = ctx.fillStyle;
    offCtx.strokeStyle = ctx.strokeStyle;
    offCtx.lineWidth = ctx.lineWidth;

    // draw the circle once ...
    offCtx.beginPath();
    offCtx.arc(pointSize / 2, pointSize / 2, radius, 0, 2 * Math.PI);
    offCtx.globalAlpha = opacity;
    offCtx.closePath();
    offCtx.fill();
    offCtx.stroke();

    const t = $currentTransform;

    // ... and then copy-paste it for every recent point in the dataset
    const positions = $latestInterestingItems.map((item) => {
      return t.apply([item.position.x, item.position.y]);
    });

    positions.forEach((position) => {
      ctx.drawImage(offCanvas, position[0] - radius, position[1] - radius, pointSize, pointSize);
    });
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
