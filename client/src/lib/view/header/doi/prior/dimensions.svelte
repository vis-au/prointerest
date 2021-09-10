<script lang="typescript">
  import { dimensions } from "$lib/state/processed-data";
  import { interestingDimensions, interestingIntervals } from "$lib/state/interesting-dimensions";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import DoiConfig from "$lib/view/header/doi/doi-config.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import Row from "$lib/widgets/row.svelte";
  import { sendInterestingDimensionRange } from "$lib/util/requests";
  import { randomlySampledItems } from "$lib/state/randomly-sampled-items";

  $: tabularData = $randomlySampledItems.map(dataItemToRecord);

  function setInterestingInterval(dimension: string, interval: [number, number]) {
    $interestingIntervals[dimension] = interval;
    sendInterestingDimensionRange(dimension, interval);
  }
</script>

<DoiConfig
  title="Select Dimension of Interest"
  message="Visualizes overall distributions in the dataset, allows defining regions of interest."
>
  {#each $dimensions as dim, i}
    <Row>
      <label for={dim}>{dim}</label>
      <input id={dim} type="checkbox" value={dim} bind:checked={$interestingDimensions[dim]} />

      {#if $interestingDimensions[dim]}
        <Histogram
          id="all-data-dim-{i}"
          data={tabularData}
          dimension={dim}
          bins={100}
          width={600}
          height={50}
          on:interval={(event) => setInterestingInterval(dim, event.detail[dim])}
        />
      {/if}
    </Row>
  {/each}
</DoiConfig>
