<script lang="typescript">
  import { colorScale } from "$lib/state/active-color-scale";
  import { activeViewMode } from "$lib/state/active-view-mode";
  import BrushLayer from "../layers/interaction/brushed-regions-layer.svelte";
  import InteractionLayer from "../layers/interaction/interaction-layer.svelte";
  import SuggestionLayer from "../layers/interaction/suggestion-layer.svelte";
  import ScatterplotView from "../layers/visualization/scatterplot-view.svelte";
  import BinnedScatterplotView from "../layers/visualization/binned-scatterplot-view.svelte";
  import Axes from "../layers/visualization/axes.svelte";
  import UiOverlay from "./ui-overlay.svelte";
  import ColorLegend from "./color-legend.svelte";
import ProgressionControls from "./progression-controls.svelte";

  export let width: number;
  export let height: number;

  let uiVisible = true;
</script>

<main style="height:{height}px">
  {#if $activeViewMode === "scatter"}
    <ScatterplotView {width} {height} />
  {:else if $activeViewMode === "binned"}
    <BinnedScatterplotView {width} {height} />
  {/if}

  <Axes {width} {height} />
  <SuggestionLayer {width} {height} />
  <BrushLayer {width} {height} />
  <InteractionLayer {width} {height} />

  {#if $activeViewMode === "binned"}
    <ColorLegend
      id="color"
      left={width - 240}
      top={height - 120}
      title=""
      blockSize={10}
      steps={10}
      bind:colorScale={$colorScale}
    />
  {/if}
  <UiOverlay {width} {height} visible={uiVisible} />
  <ProgressionControls x={width - 240} y={height - 50} />
</main>
