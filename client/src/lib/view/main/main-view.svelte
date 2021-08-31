<script lang="typescript">

import { scaleX, scaleY } from "$lib/state/scales";
import BrushLayer from "../layers/interaction/brush-layer.svelte";
import InteractionLayer from "../layers/interaction/interaction-layer.svelte";
import HintLayer from "../layers/visualization/hint-view.svelte";
import ScatterplotView from "../layers/visualization/scatterplot-view.svelte";
import BinnedScatterplotView from "../layers/visualization/binned-scatterplot-view.svelte";
import { activeViewMode } from "$lib/state/active-view-mode";
import UiOverlay from "./ui-overlay.svelte";

let innerWidth = 500;
let innerHeight = 350;
const margin = {
  horizontal: 2,
  vertical: 35
};

$: plotWidth = innerWidth - margin.horizontal;
$: plotHeight = innerHeight - margin.vertical;
$: $scaleX.range([0, plotWidth]);
$: $scaleY.range([0, plotHeight]);

let uiVisible = true;
</script>

<svelte:window bind:innerWidth={ innerWidth } bind:innerHeight={ innerHeight } />

<div class="main" on:mouseenter={ () => uiVisible = true } on:mouseleave={() => uiVisible = false }>
  { #if $activeViewMode === "scatter" }
    <ScatterplotView width={ plotWidth } height={ plotHeight } />
  { :else if $activeViewMode === "binned" }
    <BinnedScatterplotView width={ plotWidth } height={ plotHeight } />
  { /if }

  <HintLayer />
  <BrushLayer width={ plotWidth } height={ plotHeight } />
  <InteractionLayer width={ plotWidth } height={ plotHeight } />
  <UiOverlay width={ plotWidth } height={ plotHeight } visible={ uiVisible } />
</div>


<style>
  div.main {
    box-sizing: border-box;
  }
</style>