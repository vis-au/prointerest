<script lang="typescript">
  import { afterUpdate } from "svelte";

  import { hexbinning } from "$lib/state/hexbinning";
  import { hoveredBin } from "$lib/state/hovered-bin";
  import { selectedBins } from "$lib/state/selected-bins";
  import { secondaryBrushedItems } from "$lib/state/secondary-brushed-items";


  export let id: string;
  export let width: number;
  export let height: number;

  const lineWidth = 4;
  const primarySelectionColor = "rgba(255,69,0,.7)";
  const secondarySelectionColor = "rgba(255,165,0,.7)";

  let primarySelectionCanvas: HTMLCanvasElement;
  let secondarySelectionCanvas: HTMLCanvasElement;

  $: secondarySelectionBins = $hexbinning($secondaryBrushedItems);

  function renderHoveredBin(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    if (!$hoveredBin) {
      return;
    }

    const x = $hoveredBin.x;
    const y = $hoveredBin.y;

    ctx.beginPath();
    ctx.translate(x, y);
    ctx.strokeStyle = primarySelectionColor;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth * 0.5;
    ctx.setLineDash([2]);
    ctx.stroke(hexagonPath);
    ctx.fill(hexagonPath);
    ctx.translate(-x, -y);
    ctx.closePath();
    ctx.setLineDash([]);
  }

  function renderPrimarySelectedBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    ctx.beginPath();
    ctx.strokeStyle = primarySelectionColor;
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

  function renderSecondarySelectedBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
    ctx.beginPath();
    ctx.strokeStyle = secondarySelectionColor;
    ctx.fillStyle = "rgba(0, 0, 0, 0.0)";
    ctx.lineWidth = lineWidth;
    secondarySelectionBins.forEach((bin) => {
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
    renderSecondarySelectedBins(ctx, hexagonPath);

    renderHoveredBin(ctx, hexagonPath);
    renderPrimarySelectedBins(ctx, hexagonPath);
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
  <canvas
    id="{id}-selection-canvas"
    class="selection-secondary interaction-canvas"
    {width}
    {height}
    bind:this={secondarySelectionCanvas}
  />
</div>