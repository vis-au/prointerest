<script lang="ts">
  import { afterUpdate } from "svelte";
  import { currentTransform } from "$lib/state/zoom";
  import { latestChunk } from "$lib/state/latest-chunk";


  export let width: number;
  export let height: number;
  export let color = "rgba(255, 165, 0, 1)";  // fill color of points
  export let radius = 2;  // size of points

  let canvasElement: HTMLCanvasElement = null;

  function renderBins(ctx: CanvasRenderingContext2D) {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = color;

    const t = $currentTransform;

    $latestChunk.forEach(item => {
      ctx.beginPath();
      ctx.arc(t.applyX(item.position.x), t.applyY(item.position.y), radius, 0, 2 * Math.PI);
      ctx.fill();
      ctx.closePath();
    });
  }

  function render() {
    const ctx = canvasElement.getContext("2d");
    renderBins(ctx);

    return null;
  }

  afterUpdate(render);
</script>

<div id="recent-points" class="recent-points">
  <canvas id="recent-points-canvas" class="recent-points-canvas" {width} {height} bind:this={canvasElement} />
</div>

<style>
  div.recent-points {
    position: relative;
  }
  canvas.recent-points-canvas {
    position: absolute;
  }
</style>