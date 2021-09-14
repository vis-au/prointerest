<script lang="typescript">
  import { afterUpdate } from "svelte";

  import type { DoiInteraction } from "$lib/provenance/doi-interaction";
  import InteractionFactory from "$lib/provenance/doi-interaction-factory";

  import { bins } from "$lib/state/bins";
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { activeBrush } from "$lib/state/active-brush";
  import { activeInteractionMode } from "$lib/state/active-interaction-mode";
  import { getLatestTimestamp, registerNewInteraction } from "$lib/state/explored-items";
  import { hexbinning } from "$lib/state/hexbinning";
  import { hoveredBin } from "$lib/state/hovered-bin";
  import { hoveredPosition } from "$lib/state/hovered-position";
  import { sampledQuadtree } from "$lib/state/sampled-quadtree";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { selectedBins } from "$lib/state/selected-bins";
  import {
    pauseProgression,
    progressionState,
    resetProgression,
    startProgression
  } from "$lib/state/progression";
  import { currentTransform, isZooming } from "$lib/state/zoom";

  import { getDummyDataItem } from "$lib/util/dummy-data-item";
  import { getSampledPointsInRect } from "$lib/util/find-in-quadtree";

  import BrushLayer from "./brush-layer.svelte";
  import ZoomLayer from "./zoom-layer.svelte";

  export let id = "view-interaction-layer";
  export let width: number;
  export let height: number;
  export let lineWidth = 4;

  let selectionCanvas: HTMLCanvasElement;

  const color = "rgba(255,69,0,.7)";

  const interactionFactory = new InteractionFactory(width, height, $sampledQuadtree);
  interactionFactory.getItemsInRegion = getSampledPointsInRect;
  interactionFactory.getTimestamp = getLatestTimestamp;
  $: interactionFactory.width = width;
  $: interactionFactory.height = height;

  function onKeyDown(event: KeyboardEvent) {
    if (event.key === "Control") {
      $activeInteractionMode = "scat-brush";
    }
  }

  function onKeyUp(event: KeyboardEvent) {
    if (event.key === "Control") {
      $activeInteractionMode = "zoom";
    } else if (event.key === " ") {
      $progressionState === "paused" ? startProgression() : pauseProgression();
    } else if (event.key === "Backspace") {
      resetProgression();
    } else if (event.key === "Enter") {
      $isSecondaryViewCollapsed = !$isSecondaryViewCollapsed;
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
    const interaction = interactionFactory.createScatterplotBrushInteraction(x0_, y0_, x1_, y1_);
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
    className={$activeInteractionMode !== "scat-brush" ? "hidden" : ""}
    on:click={onClick}
    on:hover={onHover}
    on:end={onBrushEnd}
  />
</div>

<svelte:window on:keydown={onKeyDown} on:keyup={onKeyUp} />

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
