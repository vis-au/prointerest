<script lang="typescript">
  import { afterUpdate } from "svelte";

  import { hoveredPosition } from "$lib/state/hovered-position";
  import { selectedBins } from "$lib/state/selected-bins";
  import { currentTransform, isZooming } from "$lib/state/zoom";
  import { hexbinning } from "$lib/state/hexbinning";
  import { activeInteractionMode } from "$lib/state/active-interaction-mode";
  import InteractionFactory from "$lib/provenance/doi-interaction-factory";
  import { getDummyDataItem } from "$lib/util/dummy-data-item";
  import { quadtree } from "$lib/state/quadtree";
  import { getPointsInRect } from "$lib/util/find-in-quadtree";
  import type { DoiInteraction } from "$lib/provenance/doi-interaction";
  import { getLatestTimestamp, registerNewInteraction } from "$lib/state/explored-items";
  import { hoveredBin } from "$lib/state/hovered-bin";
  import BrushLayer from "./brush-layer.svelte";
  import ZoomLayer from "./zoom-layer.svelte";
  import { bins } from "$lib/state/bins";
  import { activeBrush } from "$lib/state/active-brush";
  import { scaleX, scaleY } from "$lib/state/scales";

  export let id = "view-interaction-layer";
  export let width: number;
  export let height: number;
  export let lineWidth = 4;

  let selectionCanvas: HTMLCanvasElement;

  const color = "rgba(255,69,0,.7)";

  const interactionFactory = new InteractionFactory(width, height, $quadtree);
  interactionFactory.getItemsInRegion = getPointsInRect;
  interactionFactory.getTimestamp = getLatestTimestamp;
  $: interactionFactory.width = width;
  $: interactionFactory.height = height;

  function buttonPressed(event: KeyboardEvent) {
    if (event.key === "Control") {
      $activeInteractionMode = "brush";
    }
  }

  function buttonReleased(event: KeyboardEvent) {
    if (event.key === "Control") {
      $activeInteractionMode = "zoom";
    }
  }

  function onInteraction(interaction: DoiInteraction) {
    registerNewInteraction(interaction);
  }

  function onBrushEnd() {
    const [[x0, y0], [x1, y1]] = $activeBrush;
    const x0_ = $scaleX(x0);
    const x1_ = $scaleX(x1);
    const y0_ = $scaleY(y0);
    const y1_ = $scaleY(y1);
    const interaction = interactionFactory.createBrushInteraction(x0_, y0_, x1_, y1_);
    onInteraction(interaction);
  }

  function onZoomEnd() {
    const interaction = interactionFactory.createZoomInteraction($currentTransform);
    onInteraction(interaction);
  }

  function onHover(event: CustomEvent) {
    const rect = event.detail.target.getBoundingClientRect();
    const x = $currentTransform.invertX(event.detail.clientX - rect.left);
    const y = $currentTransform.invertY(event.detail.clientY - rect.top);

    hoveredPosition.set([x, y]);
  }

  function onClick(event: CustomEvent) {
    const rect = event.detail.target.getBoundingClientRect();
    const x = $currentTransform.invertX(event.detail.clientX - rect.left);
    const y = $currentTransform.invertY(event.detail.clientY - rect.top);

    const dummyItem = getDummyDataItem();
    dummyItem.position = { x, y };
    const clickedBin = $hexbinning([dummyItem])[0];
    const actualBin = $bins.find((bin) => bin.x === clickedBin.x && bin.y === clickedBin.y);

    // does bin contain data?
    if (actualBin === undefined) {
      return;
    }

    // is bin already selected?
    const selectedBin = $selectedBins.find(
      (bin) => bin.x === clickedBin.x && bin.y === clickedBin.y
    );
    const selectedIndex = $selectedBins.indexOf(selectedBin);

    selectedBins.update((currentlySelectedBins) => {
      if (selectedIndex > 0) {
        // deselect
        currentlySelectedBins.splice(selectedIndex, 1);
        return currentlySelectedBins;
      } else {
        // select
        return (currentlySelectedBins = currentlySelectedBins.concat([actualBin]));
      }
    });

    const interaction = interactionFactory.createSelectInteraction(x, y);
    onInteraction(interaction);
  }

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

<div class="interaction-canvas-container {$isZooming ? 'zooming' : ''}">
  <canvas
    id="{id}-selection-canvas"
    class="selection interaction-canvas"
    {width}
    {height}
    bind:this={selectionCanvas}
  />
  <ZoomLayer
    id="zoom-layer"
    {width}
    {height}
    className={$activeInteractionMode !== "zoom" ? "hidden" : ""}
    on:click={onClick}
    on:hover={onHover}
    on:end={onZoomEnd}
  />
  <BrushLayer
    id="brush-layer"
    {width}
    {height}
    className={$activeInteractionMode !== "brush" ? "hidden" : ""}
    on:click={onClick}
    on:hover={onHover}
    on:end={onBrushEnd}
  />
</div>

<svelte:window on:keydown={buttonPressed} on:keyup={buttonReleased} />

<style>
  :global(canvas.interaction-canvas, svg.interaction-canvas) {
    position: absolute;
  }
  :global(canvas.interaction-canvas.hidden, svg.interaction-canvas.hidden) {
    display: none;
  }
  div.interaction-canvas-container {
    position: relative;
  }
  div.interaction-canvas-container.zooming {
    cursor: all-scroll;
  }
</style>
