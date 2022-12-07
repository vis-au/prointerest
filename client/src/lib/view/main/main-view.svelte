<script lang="ts">
  import { colorScale } from "$lib/state/active-color-scale";
  import { activeViewMode } from "$lib/state/active-view-mode";
  import { isRecentChunkVisible } from "$lib/state/is-recent-chunk-visible";
  import BrushLayer from "../layers/interaction/brushed-regions-layer.svelte";
  import InteractionLayer from "../layers/interaction/interaction-layer.svelte";
  import ScatterplotView from "../layers/visualization/scatterplot-view.svelte";
  import BinnedScatterplotView from "../layers/visualization/binned-scatterplot-view.svelte";
  import Axes from "../layers/visualization/axes.svelte";
  import ColorLegend from "./color-legend.svelte";
  import Tooltip from "./tooltip.svelte";
  import ViewControls from "./view-controls.svelte";
  import RecentPoints from "../layers/visualization/recent-points.svelte";
  import DecisionTreePanel from "$lib/view/main/decision-tree-panel.svelte";

  export let width: number;
  export let height: number;
</script>

<main style:height="{height}px">
  {#if $activeViewMode === "scatter"}
    <ScatterplotView {width} {height} />
  {:else if $activeViewMode === "binned"}
    <BinnedScatterplotView {width} {height} />
  {/if}

  {#if $isRecentChunkVisible}
    <RecentPoints {width} {height} />
  {/if}

  <Axes {width} {height} />
  <!-- <SuggestionLayer {width} {height} /> -->
  <BrushLayer {width} {height} />
  <InteractionLayer {width} {height} />

  <DecisionTreePanel x={40} y={80} />

  <Tooltip />

  {#if $activeViewMode === "binned"}
    <ColorLegend
      id="color"
      x={width - 240}
      y={height - 80}
      title="Bin color"
      blockSize={10}
      steps={10}
      bind:colorScale={$colorScale}
    />
  {/if}
  <ViewControls />
</main>
