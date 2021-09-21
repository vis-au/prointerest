<script lang="typescript">
  import { selectedDoiComponent } from "$lib/state/selected-doi-weight";
  import Row from "$lib/widgets/row.svelte";
  import ProgressionControls from "../main/progression-controls.svelte";

  import InterpolationComponent from "./interpolation-component.svelte";
  import PosteriorComponentWeights from "./posterior-component-weights.svelte";
  import PriorComponentWeights from "./prior-component-weights.svelte";

  export let height: number;
</script>

<header style="height:{height}px">
  <div class="title">
    <img src="static/logo.svg" alt="the ProInterest logo" height={height * 0.8} />
  </div>
  <Row>
    <InterpolationComponent />

    <Row id="doi-configuration" style="align-items:stretch;height:{height * 0.8}px;width:700px">
      {#if $selectedDoiComponent === "prior"}
        <PriorComponentWeights />
      {:else if $selectedDoiComponent === "posterior"}
        <PosteriorComponentWeights />
      {/if}
    </Row>

    <ProgressionControls useAbsolutePositioning={false} useDarkMode={true} />
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
