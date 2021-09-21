<script lang="typescript">
  import { interestingDimensions, interestingIntervals } from "$lib/state/interesting-dimensions";
  import { dimensions } from "$lib/state/processed-data";
  import { randomlySampledItems } from "$lib/state/randomly-sampled-items";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import DoiConfig from "$lib/view/header/doi/doi-panel.svelte";
  import { getDimensionExtent, sendInterestingDimensionRange } from "$lib/util/requests";
  import Column from "$lib/widgets/column.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import Row from "$lib/widgets/row.svelte";
  import { afterUpdate } from "svelte";
  import { truncateFloat } from "$lib/util/number-transform";

  let tabularData = $randomlySampledItems.map(dataItemToRecord);
  let selectedInterval: [number, number] = null;

  const extents = new Map<string, [number, number]>();

  function setInterestingInterval(dimension: string, interval: [number, number]) {
    if (interval === undefined) {
      $interestingIntervals[dimension] = null;
    } else {
      $interestingIntervals[dimension] = interval;
    }
    sendInterestingDimensionRange(dimension, interval);
  }

  function getSelectedDimensionExtents() {
    Object.keys($interestingDimensions)
      .filter((d) => $interestingDimensions[d])
      .forEach((d) => {
        if (extents[d] === undefined) {
          getDimensionExtent(d).then((extent) => {
            extents[d] = [extent.min, extent.max];
          });
        }
      });
  }

  afterUpdate(() => {
    getSelectedDimensionExtents();
  });
</script>

<DoiConfig
  title="Select Dimension of Interest"
  message="Visualizes overall distributions in the dataset, allows defining regions of interest."
>
  {#each $dimensions as dim, i}
    <Column style="margin:10px 0">
      <Row>
        <label for={dim}>{dim}</label>
        <input id={dim} type="checkbox" value={dim} bind:checked={$interestingDimensions[dim]} />

        <span class="interesting-range">
          {#if $interestingDimensions[dim] && $interestingIntervals[dim] !== null}
            [
            {truncateFloat($interestingIntervals[dim][0])},
            {truncateFloat($interestingIntervals[dim][1])}
            ]
          {/if}
        </span>
      </Row>

      {#if $interestingDimensions[dim]}
        <Histogram
          id="all-data-dim-{i}"
          data={tabularData}
          dimension={dim}
          domain={extents[dim]}
          selectedValues={$interestingIntervals[dim]}
          bins={100}
          width={550}
          height={50}
          on:interval={(event) => selectedInterval = event.detail[dim]}
          on:end={() => setInterestingInterval(dim, selectedInterval)}
        />
      {/if}
    </Column>
  {/each}
</DoiConfig>

<style>
  span.interesting-range {
    color: #666;
    margin-left: 10px;
  }
</style>
