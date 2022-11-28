<script lang="ts">
  import { afterUpdate } from "svelte";
  import { interestingIntervals, selectedDoiDimensions } from "$lib/state/interesting-dimensions";
  import { randomlySampledItems } from "$lib/state/randomly-sampled-items";
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import DoiConfig from "$lib/view/header/doi/doi-panel.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import Row from "$lib/widgets/row.svelte";
  import { truncateFloat } from "$lib/util/number-transform";
  import { getDimensionExtent } from "$lib/util/requests";
  import type { DOIDimension } from "$lib/types/doi-dimension";

  let selectedInterval: [number, number] = null;
  let usePresetInterval = false;

  $: tabularData = $randomlySampledItems.map(dataItemToRecord);

  const extents = new Map<string, [number, number]>();


  function setInterestingInterval(dimension: string, interval: [number, number]) {
    if (interval === undefined) {
      $interestingIntervals[dimension] = null;
    } else {
      $interestingIntervals[dimension] = interval;
    }
    // TODO: send the right info to the backend
    // sendInterestingDimensionRange(dimension, interval);
  }

  function getSelectedDimensionExtents() {
    $selectedDoiDimensions.forEach((d) => {
      if (extents[d] === undefined) {
        getDimensionExtent(d).then((extent) => {
          extents[d] = [extent.min, extent.max];
        });
      }
    });
  }

  afterUpdate(getSelectedDimensionExtents);

  selectedDoiWeight.subscribe((newSelection: DOIDimension) => {
    if (newSelection === null || newSelection === undefined) {
      usePresetInterval = true;
    }
  });
</script>

<DoiConfig on:close
  title="Select interesting range"
  message="Items with values in that range along this dimension get a higher degree of interest."
>
  <Row>
    {#if !!$interestingIntervals[$selectedDoiWeight]}
      <span>Selected range:</span>
      <span class="interesting-range">
        [{truncateFloat($interestingIntervals[$selectedDoiWeight][0])},
        {truncateFloat($interestingIntervals[$selectedDoiWeight][1])}]
      </span>
    {:else}
      <span class="no-interesting-range">Use brushing to select range:</span>
    {/if}
  </Row>

  <Histogram
    id="all-data-dim-{$selectedDoiWeight}"
    data={tabularData}
    dimension={$selectedDoiWeight}
    domain={extents[$selectedDoiWeight]}
    selectedInterval={$interestingIntervals[$selectedDoiWeight]}
    bins={100}
    width={550}
    height={100}
    bind:usePresetInterval={usePresetInterval}
    on:interval={(event) => (selectedInterval = event.detail[$selectedDoiWeight])}
    on:end={() => setInterestingInterval($selectedDoiWeight, selectedInterval)}
  />
</DoiConfig>

<style>
  span.interesting-range {
    margin-left: 10px;
    font-family: "Courier New", Courier, monospace;
  }
</style>
