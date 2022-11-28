<script lang="ts">
  import { dimensions } from "$lib/state/processed-data";
  import { doiDimensionWeights, isDimensionInteresting, selectedDoiDimensions } from "$lib/state/interesting-dimensions";
  import type { DOIDimension } from "$lib/types/doi-dimension";
  import { sendDimenionWeights } from "$lib/util/requests";
  import Row from "$lib/widgets/row.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import Options from "$lib/widgets/options.svelte";
  import ProgressionControls from "./progression-controls.svelte";
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";

  export let height: number;

  const maxWidth = 700;
  let selectedDimensionWeights = new Map<DOIDimension, number>();

  $: selectedDimensionWeights.forEach((value, key) => $doiDimensionWeights.set(key, value));
  $: $selectedDoiDimensions = $dimensions.filter((d) => $isDimensionInteresting[d]);

  selectedDoiDimensions.subscribe((newDimension) => {
    selectedDimensionWeights = new Map();
    newDimension.forEach((dimension) => {
      selectedDimensionWeights.set(dimension, $doiDimensionWeights.get(dimension));
    });
  });

  function removeDimension(event: CustomEvent<string>) {
    $isDimensionInteresting[event.detail] = false;
  }
</script>

<header style="height:{height}px">
  <div class="title">
    <img src="static/logo.svg" alt="the ProInterest logo" height={height * 0.8} />
  </div>
  <Row>
    <Row id="doi-configuration" style="align-items:center;height:{height * 0.8}px;flex-grow: 5">
      <h2>DOI features:</h2>
      <WeightedValues
        id="selected-doi-dimensions"
        totalSize={maxWidth}
        weightsRemovable={true}
        useDarkmode={true}
        backgroundColor="#008080"
        isSelectable={true}
        bind:valueWeights={selectedDimensionWeights}
        bind:activeWeight={$selectedDoiWeight}
        on:remove-weight={removeDimension}
        on:end={() => sendDimenionWeights($doiDimensionWeights)}
      />
      <Options
        options={$dimensions}
        showActive={false}
        showInactive={false}
        bind:activeOptions={$isDimensionInteresting}
        useDarkMode={true}
        style="margin-left: 25px"
      />
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
    font-weight: bold;;
  }

  header div.title {
    margin-left: 2px;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
</style>
