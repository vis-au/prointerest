<script lang="ts">
  import type { DoiInteraction } from "$lib/provenance/doi-interaction";
  import InteractionFactory from "$lib/provenance/doi-interaction-factory";
  import { interactionLog } from "$lib/provenance/interaction-log";
  import type ScatterplotBrush from "$lib/provenance/scatterplot-brush-interaction";
  import type ScatterplotLassoBrush from "$lib/provenance/scatterplot-lasso-brush-interaction";

  import { bins } from "$lib/state/bins";
  import { activeBrush, activeLasso } from "$lib/state/active-brush";
  import { activeDecisionTree } from "$lib/state/active-decision-tree";
  import { activeInteractionMode } from "$lib/state/active-interaction-mode";
  import { hexbinning } from "$lib/state/hexbinning";
  import { hoveredPosition } from "$lib/state/hovered-position";
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { dimensions } from "$lib/state/processed-data";
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
  import { getPointsInPolygon, getPointsInRect } from "$lib/util/find-in-quadtree";
  import { getDecisionTree, getRegressionTree } from "$lib/util/requests";

  import BrushLayer from "./brush-layer.svelte";
  import SelectionLayer from "./selection-layer.svelte";
  import ZoomLayer from "./zoom-layer.svelte";

  export let width: number;
  export let height: number;

  const interactionFactory = new InteractionFactory(width, height, $sampledQuadtree);
  $: interactionFactory.quadtree = $sampledQuadtree;
  interactionFactory.getItemsInRegion = getPointsInRect;
  interactionFactory.getItemsInPolygon = getPointsInPolygon;
  interactionFactory.getTimestamp = $interactionLog.getLatestTimestamp;
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
    $interactionLog.add(interaction);
  }

  async function _steer(brushInteraction: ScatterplotBrush | ScatterplotLassoBrush) {
    const interesting = brushInteraction.getAffectedItems();

    // find data to train against, by finding (at most twice as many) uninteresting items
    const uninteresting = $sampledQuadtree.data()
      .filter((item) => interesting.indexOf(item) === -1)
      .filter((_, i) => i < interesting.length*2);

    $activeDecisionTree = await getDecisionTree(interesting, uninteresting, $dimensions);
  }

  async function steer(brushInteraction: ScatterplotBrush | ScatterplotLassoBrush) {
    const interesting = brushInteraction.getAffectedItems();

    const scores = Array.from({length: interesting.length}).map(Math.random);

    $activeDecisionTree = await getRegressionTree(interesting, scores, $dimensions);
  }

  function onBrushEnd() {
    // can be null when using the lasso brush
    if ($activeBrush !== null) {
      const [[x0, y0], [x1, y1]] = $activeBrush;
      const x0_ = $scaleX(x0);
      const x1_ = $scaleX(x1);
      const y0_ = $scaleY(y0);
      const y1_ = $scaleY(y1);
      const interaction = interactionFactory.createScatterplotBrushInteraction(x0_, y0_, x1_, y1_);
      onInteraction(interaction);
      steer(interaction);  // FIXME: steers every time user brushes
    } else if ($activeLasso !== null) {
      const polygon = $activeLasso.map(
        (pos) => [$scaleX(pos[0]), $scaleY(pos[1])] as [number, number]
      );
      const interaction = interactionFactory.createLassoBrushInteraction(polygon);
      onInteraction(interaction);
      steer(interaction);  // FIXME: steers every time user brushes
    }
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
</script>

<div class="interaction-canvas-container {$isZooming ? 'zooming' : ''}">
  <SelectionLayer id="selection-layer" {width} {height} />
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
  :global(.interaction-canvas) {
    position: absolute;
  }
  :global(.interaction-canvas.hidden) {
    display: none;
  }
  div.interaction-canvas-container {
    position: relative;
  }
  div.interaction-canvas-container.zooming {
    cursor: all-scroll;
  }
</style>
