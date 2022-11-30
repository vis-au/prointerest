<script lang="ts">
  import { isDimensionInteresting, interestingIntervals } from "$lib/state/interesting-dimensions";
  import { dimensions } from "$lib/state/processed-data";
  import { randomDataSubset } from "$lib/state/sampled-data";
  import DoiConfig from "$lib/view/header/doi/doi-panel.svelte";
  import { getDimensionExtent, sendInterestingDimensionRange } from "$lib/util/requests";
  import Column from "$lib/widgets/column.svelte";
  import DoiItemHistogram from "$lib/view/main/doi-item-histogram.svelte";
  import Row from "$lib/widgets/row.svelte";
  import { afterUpdate } from "svelte";
  import { truncateFloat } from "$lib/util/number-transform";

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
    Object.keys($isDimensionInteresting)
      .filter((d) => $isDimensionInteresting[d])
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
        <input id={dim} type="checkbox" value={dim} bind:checked={$isDimensionInteresting[dim]} />

        <span class="interesting-range">
          {#if $isDimensionInteresting[dim] && $interestingIntervals[dim] !== null}
            [
            {truncateFloat($interestingIntervals[dim][0])},
            {truncateFloat($interestingIntervals[dim][1])}
            ]
          {/if}
        </span>
      </Row>

      {#if $isDimensionInteresting[dim]}
        <DoiItemHistogram
          id="all-data-dim-{i}"
          data={$randomDataSubset}
          dimension={dim}
          domain={extents[dim]}
          selectedInterval={$interestingIntervals[dim]}
          bins={100}
          width={550}
          height={50}
          on:interval={(event) => (selectedInterval = event.detail[dim])}
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
