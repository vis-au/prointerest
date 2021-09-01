<script lang="typescript">

import { scaleX, scaleY } from "$lib/state/scales";
import BrushLayer from "../layers/interaction/brush-layer.svelte";
import InteractionLayer from "../layers/interaction/interaction-layer.svelte";
import HintLayer from "../layers/visualization/hint-view.svelte";
import ScatterplotView from "../layers/visualization/scatterplot-view.svelte";
import BinnedScatterplotView from "../layers/visualization/binned-scatterplot-view.svelte";
import { activeViewMode } from "$lib/state/active-view-mode";
import UiOverlay from "./ui-overlay.svelte";

export let plotWidth: number;
export let plotHeight: number;

let uiVisible = true;
</script>

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