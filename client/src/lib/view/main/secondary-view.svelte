<script lang="typescript">
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { dimensions } from "$lib/state/processed-data";
  import { interestingDimensions } from "$lib/state/interesting-dimensions";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import Column from "$lib/widgets/column.svelte";
  import Options from "$lib/widgets/options.svelte";
  import Row from "$lib/widgets/row.svelte";
  import ControlButton from "./control-button.svelte";
  import { selectedItems } from "$lib/state/selected-items";
  import MultiHistogram from "$lib/widgets/multi-histogram.svelte";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import { randomlySampledItems } from "$lib/state/randomly-sampled-items";

  export let width: number;
  export let height: number;

  let histogramMode: "selected"|"all" = "all";

  $: items = histogramMode === "all"
    ? $randomlySampledItems
    : $selectedItems;

  $: data = items.map(dataItemToRecord);
</script>

<Column id="secondary-view" style="max-width:{width}px;height:{height}px">
  <Row id="secondary-header" style="margin-bottom: 25px">
    <Row>
      <Row style="margin-right:20px;padding-bottom:3px">
        <h2>Mode:</h2>
        <Alternatives
          name="active-histogram-mode"
          alternatives={["selected", "all"]}
          bind:activeAlternative={histogramMode}
        />
      </Row>
      <Options
        options={$dimensions}
        showInactive={false}
        bind:activeOptions={$interestingDimensions}
      />
    </Row>
    <ControlButton on:click={ () => $isSecondaryViewCollapsed = true }>close</ControlButton>
  </Row>
  <Row id="selected-data-histograms"style="width:{width}px">
    <MultiHistogram
      id="secondary-selected-dims"
      data={data}
      dimensions={Object.keys($interestingDimensions).filter(d => $interestingDimensions[d])}
      showTitle={false}
      groupDimension="selected"
      width={310}
      height={height * .4}
    />
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
    padding-bottom: 20px;
  }
  h2 {
    font-size: 12pt;
    margin: 0;
  }
</style>