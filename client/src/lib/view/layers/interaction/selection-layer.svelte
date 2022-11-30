<script lang="ts">
  import { afterUpdate } from "svelte";

  import { hexbinning } from "$lib/state/hexbinning";
  import { hoveredBin } from "$lib/state/hovered-bin";
  import { selectedBins } from "$lib/state/selected-bins";
  import { selectionInSecondaryView } from "$lib/state/secondary-brushed-items";

  export let id: string;
  export let width: number;
  export let height: number;

  const lineWidth = 4;
  const color = "rgba(255,165,0,.7)";
  const hoverColor = "rgba(255,65,0,.7)";

  let primarySelectionCanvas: HTMLCanvasElement;

  $: binsWithSelectedItems = $hexbinning($selectionInSecondaryView);

  function renderHoveredBin(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    if (!$hoveredBin) {
      return;
    }

    const x = $hoveredBin.x;
    const y = $hoveredBin.y;

    ctx.beginPath();
    ctx.translate(x, y);
    ctx.strokeStyle = hoverColor;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth * 0.5;
    ctx.setLineDash([2]);
    ctx.stroke(hexagonPath);
    ctx.fill(hexagonPath);
    ctx.translate(-x, -y);
    ctx.closePath();
    ctx.setLineDash([]);
  }

  function renderClickSelection(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
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

  function renderSecondaryViewSelection(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth;
    binsWithSelectedItems.forEach((bin) => {
      ctx.translate(bin.x, bin.y);
      ctx.stroke(hexagonPath);
      ctx.fill(hexagonPath);
      ctx.translate(-bin.x, -bin.y);
    });
    ctx.closePath();
  }

  function render() {
    if (!primarySelectionCanvas) {
      return;
    }

    const hexagonPath = new Path2D($hexbinning.hexagon());
    const ctx = primarySelectionCanvas.getContext("2d");
    ctx.clearRect(0, 0, width, height);

    // make sure clicked bin is always visible, so render secondary selection first
    renderSecondaryViewSelection(ctx, hexagonPath);
    renderClickSelection(ctx, hexagonPath);
    renderHoveredBin(ctx, hexagonPath);
  }

  afterUpdate(render);
</script>

<div class="selection-layer">
  <canvas
    id="{id}-selection-canvas"
    class="selection-main interaction-canvas"
    {width}
    {height}
    bind:this={primarySelectionCanvas}
  />
</div>
