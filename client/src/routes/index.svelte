<script lang="typescript">
import { range } from "d3-array";

import { dimensions, processedData } from "$lib/state/processed-data";
import type { BinType } from "$lib/types/bin-type";
import Header from "$lib/view/header/header.svelte";
import MainView from "$lib/view/main/main-view.svelte";
import { onMount } from "svelte";
import { hexbinning } from "$lib/state/hexbinning";
import { currentTransform } from "$lib/state/zoom";
import ActiveDoiPanel from "$lib/view/header/doi/active-doi-panel.svelte";

const data = range(0, 10000).map(() => [Math.random(), Math.random(), Math.random()] as BinType);
$processedData = data;
$dimensions = ["dimension a", "dimension b", "dimension c"]

onMount(() => {
  setTimeout(() => {
    // triggers the rendering of the binned scatterplot
    $hexbinning = $hexbinning;
    // triggers the rendering of the scatterplot
    $currentTransform = $currentTransform;
  }, 0);
});

</script>


<div id="pro-interest">
  <Header />
  <MainView />
  <ActiveDoiPanel />
</div>


<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
  :global(body *) {
    font-family: Roboto;
    box-sizing: border-box;
  }
</style>
