<script lang="ts">
  import { colorScale } from "$lib/state/active-color-scale";
  import { activeViewMode } from "$lib/state/active-view-mode";
  import { isRecentChunkVisible } from "$lib/state/is-recent-chunk-visible";
  import DecisionTreePanel from "$lib/view/main/decision-tree-panel.svelte";
  import BrushLayer from "../layers/interaction/brushed-regions-layer.svelte";
  import InteractionLayer from "../layers/interaction/interaction-layer.svelte";
  import Axes from "../layers/visualization/axes.svelte";
  import BinnedScatterplotView from "../layers/visualization/binned-scatterplot-view.svelte";
  import RecentPoints from "../layers/visualization/recent-points.svelte";
  import ScatterplotView from "../layers/visualization/scatterplot-view.svelte";
  import ColorLegend from "./color-legend.svelte";
  import Tooltip from "./tooltip.svelte";
  import ViewControls from "./view-controls.svelte";

  export let width: number;
  export let height: number;
</script>

<main style:height="{height}px" style="position:relative">
  {#if $activeViewMode === "scatter"}
    <ScatterplotView {width} {height} />
  {:else if $activeViewMode === "binned"}
    <BinnedScatterplotView {width} {height} />
  {/if}

  {#if $isRecentChunkVisible}
    <RecentPoints {width} {height} useBinning={$activeViewMode === "binned"} />
  {/if}

  <Axes {width} {height} />
  <!-- <SuggestionLayer {width} {height} /> -->
  <BrushLayer {width} {height} />
  <InteractionLayer {width} {height} />

  <Tooltip />

  <DecisionTreePanel x={10} y={90} />

  <ColorLegend
    id="color"
    x={width - 240}
    y={height - 100}
    title="Bin color"
    blockSize={10}
    steps={10}
    bind:colorScale={$colorScale}
  />
  <ViewControls />
</main>
