<script lang="ts">
  import {
      doiDimensionWeights,
      isDimensionInteresting,
      selectedDoiDimensions
  } from "$lib/state/interesting-dimensions";
  import { dimensions } from "$lib/state/processed-data";
  import { isDoiFunctionDirty, useOurDoiApproach } from "$lib/state/progression";
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
  import type { DOIDimension } from "$lib/types/doi-dimension";
  import { sendDimenionWeights } from "$lib/util/requests";
  import Options from "$lib/widgets/options.svelte";
  import Row from "$lib/widgets/row.svelte";
  import Toggle from "$lib/widgets/toggle.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import ProgressionControls from "./progression-controls.svelte";

  export let height: number;
  let width: number;

  let selectedDimensionWeights = new Map<DOIDimension, number>();

  $: {
    selectedDimensionWeights.forEach((value, key) => $doiDimensionWeights.set(key, value));
    $doiDimensionWeights = $doiDimensionWeights;
  }
  $: $selectedDoiDimensions = $dimensions.filter((d) => $isDimensionInteresting[d]);

  selectedDoiDimensions.subscribe((newSelection) => {
    selectedDimensionWeights = new Map();
    newSelection.forEach((dimension) => {
      selectedDimensionWeights.set(dimension, $doiDimensionWeights.get(dimension));
    });
  });

  function removeDimension(event: CustomEvent<string>) {
    $isDimensionInteresting[event.detail] = false;
  }

  function onDimensionWeightsChanged() {
    sendDimenionWeights($doiDimensionWeights);
    $isDoiFunctionDirty = true;
  }
</script>

<header style="height:{height}px" bind:clientWidth={width}>
  <div class="title">
    <img src="static/logo.svg" alt="the ProInterest logo" height={height * 0.8} />
  </div>
  <Row>
    <Row id="doi-configuration" style="align-items:center;height:{height * 0.8}px;flex-grow: 5">
      <h2>DOI features:</h2>
      <WeightedValues
        id="selected-doi-dimensions"
        totalSize={width * 0.35}
        weightsRemovable={true}
        useDarkmode={true}
        backgroundColor="#008080"
        isSelectable={true}
        bind:valueWeights={selectedDimensionWeights}
        bind:activeWeight={$selectedDoiWeight}
        on:remove-weight={removeDimension}
        on:end={onDimensionWeightsChanged}
      />
      <Options
        options={$dimensions}
        showActive={false}
        showInactive={false}
        bind:activeOptions={$isDimensionInteresting}
        useDarkMode={true}
        style="margin-left: 25px"
      />
      <Toggle bind:active={$useOurDoiApproach} style="max-width:{width*0.1}px;overflow:hidden">optimize DOI</Toggle>
    </Row>
  </Row>
  <ProgressionControls useAbsolutePositioning={false} useDarkMode={true} style="flex-grow:0" />
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

  h2 {
    margin: 0;
    margin-right: 25px;
    padding: 0;
    font-size: 18px;
    font-weight: bold;
  }

  header div.title {
    margin-left: 2px;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
</style>
