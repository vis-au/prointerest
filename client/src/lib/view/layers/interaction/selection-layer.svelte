<script lang="typescript">
  import { afterUpdate } from "svelte";

  import { hexbinning } from "$lib/state/hexbinning";
  import { hoveredBin } from "$lib/state/hovered-bin";
  import { selectedBins } from "$lib/state/selected-bins";


  export let id: string;
  export let width: number;
  export let height: number;

  const lineWidth = 4;
  const color = "rgba(255,69,0,.7)";

  let selectionCanvas: HTMLCanvasElement;

  function renderHoveredBin(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    if (!$hoveredBin) {
      return;
    }

    const x = $hoveredBin.x;
    const y = $hoveredBin.y;

    ctx.beginPath();
    ctx.translate(x, y);
    ctx.strokeStyle = color;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth * 0.5;
    ctx.setLineDash([2]);
    ctx.stroke(hexagonPath);
    ctx.fill(hexagonPath);
    ctx.translate(-x, -y);
    ctx.closePath();
    ctx.setLineDash([]);
  }

  function renderSelectedBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth;
    $selectedBins.forEach((bin) => {
      ctx.translate(bin.x, bin.y);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
  }

  function render() {
    if (!selectionCanvas) {
      return;
    }

    const hexagonPath = new Path2D($hexbinning.hexagon());
    const ctx = selectionCanvas.getContext("2d");
    ctx.clearRect(0, 0, width, height);

    renderHoveredBin(ctx, hexagonPath);
    renderSelectedBins(ctx, hexagonPath);
  }

  afterUpdate(render);
</script>

<canvas
  id="{id}-selection-canvas"
  class="selection interaction-canvas"
  {width}
  {height}
  bind:this={selectionCanvas}
/>