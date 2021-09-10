<script lang="typescript">
  import { updateExploredItems } from "$lib/state/explored-items";
  import { activeDoiValues } from "$lib/state/latest-doi-values";
  import { quadtree } from "$lib/state/quadtree";
  import { selectedDoiComponent } from "$lib/state/selected-doi-weight";
  import { getDoiValues } from "$lib/util/requests";
  import Row from "$lib/widgets/row.svelte";

  import ControlButton from "../../widgets/control-button.svelte";
  import InterpolationComponent from "./interpolation-component.svelte";
  import PosteriorComponentWeights from "./posterior-component-weights.svelte";
  import PriorComponentWeights from "./prior-component-weights.svelte";

  export let height: number;

  async function evaluateInterest() {
    updateExploredItems();
    const doiValues = await getDoiValues($quadtree.data());
    const map = new Map<number, number>();
    doiValues.forEach((pair) => map.set(pair[0], pair[1]));
    $activeDoiValues = map;
  }
</script>

<header style="height:{height}px">
  <div class="title">
    <img src="static/logo.svg" alt="the ProInterest logo" height={height*.8} />
  </div>
  <Row>
    <InterpolationComponent />

    <Row id="doi-configuration" style="align-items:stretch;height:{height*.8}px;width:700px">
      {#if $selectedDoiComponent === "prior"}
        <PriorComponentWeights />
      {:else if $selectedDoiComponent === "posterior"}
        <PosteriorComponentWeights />
      {/if}
    </Row>

    <ControlButton
      style="background:#666;font-weight:bold;margin:0 10px 0 20px;padding:5px 10px"
      on:click={evaluateInterest}
    >
      Compute Interest
    </ControlButton>
  </Row>
</header>

<style>
  header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    background: #333;
    color: #fff;
    border-bottom: 1px solid #ddd;
  }

  header div.title {
    margin-left: 2px;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
</style>
