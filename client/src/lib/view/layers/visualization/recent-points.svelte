<script lang="ts">
  import { afterUpdate } from "svelte";
  import { currentTransform } from "$lib/state/zoom";
  import { latestInterestingItems } from "$lib/state/latest-chunk";

  export let width: number;
  export let height: number;
  export let color = "rgba(255, 255, 255, 0.73)";  // black color of points
  export let radius = 4;  // size of points

  let canvasElement: HTMLCanvasElement = null;

  function render() {
    const ctx = canvasElement.getContext("2d");
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = color;
    ctx.strokeStyle = "rgba(0, 0, 0, 0.73)";
    ctx.lineWidth = 2;

    const t = $currentTransform;

    $latestInterestingItems.forEach(item => {
      ctx.beginPath();
      ctx.arc(t.applyX(item.position.x), t.applyY(item.position.y), radius, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();
      ctx.closePath();
    });
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