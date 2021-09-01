<script lang="typescript">
import GuidanceProvider from "$lib/doi/guidance-provider";

import { activeIndicateMode } from "$lib/state/active-indicate-mode";

import { hexbinning } from "$lib/state/hexbinning";
import { interestingItems } from "$lib/state/interesting-items";
import { viewPort as vp } from "$lib/state/visible-data";
import { afterUpdate } from "svelte";


export let width;
export let height;

const guide = new GuidanceProvider();

$: hintItems = $activeIndicateMode === "explored" ? $interestingItems
  : $activeIndicateMode === "similar" ? guide.getItemsSimilarToInterest($interestingItems)
  : $activeIndicateMode === "dissimilar" ? guide.getItemsDissimilarToInterest($interestingItems)
  : [];

$: bins = $hexbinning(hintItems);
$: visibleBins = bins.filter(bin => {
  return bin.x > $vp.minX && bin.x < $vp.maxX && bin.y > $vp.minY && bin.y < $vp.maxY;
});
$: offscreenBins = bins.filter(bin => {
  return visibleBins.indexOf(bin) === -1;
});


let canvas: HTMLCanvasElement;
const arrowPadding = 10;

function renderVisibleGuides(ctx: CanvasRenderingContext2D) {
    const hexagonPath = new Path2D($hexbinning.hexagon());

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "rgba(255,255,255,0.1)";
    ctx.strokeStyle="rgba(255,199,0,1)";
    ctx.lineWidth = 4;

    ctx.beginPath();
    visibleBins.forEach(bin => {
      ctx.translate(bin.x, bin.y);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
}

function renderOffscreenGuides(ctx: CanvasRenderingContext2D) {
  ctx.fillStyle = "rgba(255,199,0,1)";
  const w = 30;
  const triangle = new Path2D(`M0,0L${w},0L${w/2},${w*.6}Z`);

  ctx.beginPath();
  offscreenBins.forEach(bin => {
    let { x, y } = bin;
    let rot = 0;

    if (x < 0) {
      x = arrowPadding + arrowPadding;
      rot = Math.PI * .5;
    } else if (x > width) {
      x = width - arrowPadding - arrowPadding;
      rot = Math.PI * 1.5;
    }
    if (y < 0) {
      y = arrowPadding + arrowPadding;
      rot = Math.PI;
    } else if (y > height) {
      y = height - arrowPadding - arrowPadding;
    }

    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.fill(triangle);
    ctx.rotate(-rot);
    ctx.translate(-x, -y);
  });
  ctx.closePath();
}

function render() {
  const ctx = canvas.getContext("2d");

  renderVisibleGuides(ctx);
  renderOffscreenGuides(ctx);
}

afterUpdate(render);
</script>

<div class="hint-view">
  <canvas
    id="hint-canvas"
    { width }
    { height }
    bind:this={ canvas }
  />
</div>

<style>
  div.hint-view {
    position: relative;
  }
  div.hint-view canvas {
    position: absolute;
  }
</style>