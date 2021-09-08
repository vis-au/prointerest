<script lang="typescript">
  import { activeBrush } from "$lib/state/active-brush";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { currentTransform } from "$lib/state/zoom";

  import { afterUpdate } from "svelte";

  export let width: number;
  export let height: number;

  let canvas: HTMLCanvasElement;

  afterUpdate(render);

  function render() {
    const t = $currentTransform;

    const [[_x0, _y0], [_x1, _y1]] = $activeBrush;
    const x0 = t.applyX($scaleX(_x0));
    const y0 = t.applyY($scaleY(_y0));
    const x1 = t.applyX($scaleX(_x1));
    const y1 = t.applyY($scaleY(_y1));

    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.strokeStyle = "rgba(0,0,0,0.73)";
    ctx.rect(x0, y0, Math.abs(x0 - x1), Math.abs(y0 - y1));
    ctx.stroke();
    ctx.closePath();
  }
</script>

<canvas id="active-brush-layer" {width} {height} bind:this={canvas} />

<style>
  canvas#active-brush-layer {
    position: absolute;
  }
</style>
