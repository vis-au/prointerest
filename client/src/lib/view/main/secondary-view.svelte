<script lang="typescript">
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { dimensions } from "$lib/state/processed-data";
  import { dimensionInterestRecord } from "$lib/state/selected-dimensions-of-interest";
  import { selectedItems } from "$lib/state/selected-items";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import Column from "$lib/widgets/column.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import Options from "$lib/widgets/options.svelte";
  import Row from "$lib/widgets/row.svelte";
  import ControlButton from "./control-button.svelte";

  export let width: number;
  export let height: number;

  $: tabularData = $selectedItems.map(dataItemToRecord);
</script>

<Column id="secondary-view" style="max-width:{width}px;height:{height}px">
  <Row id="secondary-header" style="margin-bottom: 25px">
    <Row>
      <Options
        options={$dimensions}
        showInactive={false}
        bind:activeOptions={$dimensionInterestRecord}
      />
    </Row>
    <ControlButton on:click={ () => $isSecondaryViewCollapsed = true }>close</ControlButton>
  </Row>
  <Row id="selected-data-histograms"style="width:{width}px">
    {#each Object.keys($dimensionInterestRecord).filter(d => $dimensionInterestRecord[d]) as dim, i}
      <div class="dimension">
        <Histogram
          id="secondary-selected-dim-{dim}"
          data={tabularData}
          dimension={$dimensions.indexOf(dim) + ""}
          showTitle={false}
          width={310}
          height={height * .4}
        />
        <h3>{dim}</h3>
      </div>
    {/each}
  </Row>
</Column>

<style>
  :global(#secondary-view) {
    overflow: hidden;
    justify-content: space-between;
    flex-wrap: nowrap
  }
  :global(#secondary-header) {
    min-width: 100%;
    border-top: 2px solid #333;
    border-bottom: 1px solid #efefef;
    padding: 10px;
    justify-content: space-between;
    flex-wrap: nowrap;
  }
  :global(#selected-data-histograms) {
    overflow-x: auto;
    overflow-y: hidden;
    flex-wrap: nowrap;
    padding-bottom: 10px;
  }
  h3 {
    font-size: 10pt;
    text-align: center;
    margin: 0;
  }
</style>