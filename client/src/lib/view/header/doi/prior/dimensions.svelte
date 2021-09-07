<script lang="typescript">
  import { dimensions } from "$lib/state/processed-data";
  import { quadtree } from "$lib/state/quadtree";
  import { dimensionInterestRecord } from "$lib/state/selected-dimensions-of-interest";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import DoiConfig from "$lib/widgets/doi-config.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import Row from "$lib/widgets/row.svelte";

  $: tabularData = $quadtree.data().map(dataItemToRecord);
</script>

<DoiConfig
  width={400}
  title="Select Dimension of Interest"
  message="Visualizes overall distributions in the dataset, allows defining regions of interest."
>
  {#each $dimensions as dim, i}
    <Row>
      <label for={dim}>{dim}</label>
      <input id={dim} type="checkbox" value={dim} bind:checked={$dimensionInterestRecord[dim]} />

      {#if $dimensionInterestRecord[dim]}
        <Histogram
          id="all-data-dim-{i}"
          data={tabularData}
          dimension={i + ""}
          width={300}
          height={50}
        />
      {/if}
    </Row>
  {/each}
</DoiConfig>
