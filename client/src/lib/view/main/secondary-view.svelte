<script lang="typescript">
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { dimensions } from "$lib/state/processed-data";
  import { selectedDimensionsOfInterest } from "$lib/state/selected-dimensions-of-interest";
  import { selectedItems } from "$lib/state/selected-items";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import Column from "$lib/widgets/column.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import Options from "$lib/widgets/options.svelte";
  import Row from "$lib/widgets/row.svelte";
  import { afterUpdate } from "svelte";
  import ControlButton from "./control-button.svelte";

  export let width: number;
  export let height: number;

  $: tabularData = $selectedItems.map(dataItemToRecord);

  $: selectedDimensions = {};
  $: $selectedDimensionsOfInterest = Object.keys(selectedDimensions)
      .filter(d => selectedDimensions[d]);

  afterUpdate(() => {
    $selectedDimensionsOfInterest.forEach(dim => selectedDimensions[dim] = true);
  });
</script>

<Column id="secondary-view" style="max-width:{width}px;height:{height}px">
  <Row id="secondary-header" style="margin-bottom: 25px">
    <Row>
      <Options
        options={$dimensions}
        bind:activeOptions={selectedDimensions}
        showInactive={false}
      />
    </Row>
    <ControlButton on:click={ () => $isSecondaryViewCollapsed = true }>close</ControlButton>
  </Row>
  <Row style="width:{width}px;overflow-x:auto;overflow-y:hidden;flex-wrap:nowrap">
    {#each $selectedDimensionsOfInterest as dim, i}
      <div class="dimension">
        <Histogram
          id="secondary-selected-dim-{dim}"
          data={tabularData}
          dimension={i+""}
          showTitle={false}
          width={310}
          height={50}
        />
        <h3>{dim}</h3>
      </div>
    {/each}
  </Row>
</Column>

<style>
  :global(#secondary-view) {
    overflow: hidden;
    padding: 10px 0;
    justify-content: space-between;
    flex-wrap: nowrap
  }
  :global(#secondary-header) {
    min-width: 100%;
    border-bottom: 1px solid #ccc;
    padding: 0 5px;
    padding-bottom: 10px;
    justify-content: space-between;
    flex-wrap: nowrap;
  }
  h3 {
    font-size: 10pt;
    text-align: center;
  }
</style>