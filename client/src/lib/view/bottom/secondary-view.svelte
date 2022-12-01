<script lang="ts">
  import InteractionFactory from "$lib/provenance/doi-interaction-factory";
  import type HistogramBrushInteraction from "$lib/provenance/histogram-brush-interaction";
  import { interactionLog } from "$lib/provenance/interaction-log";
  import { selectedDoiDimensions } from "$lib/state/interesting-dimensions";
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { dimensions } from "$lib/state/processed-data";
  import { quadtree } from "$lib/state/quadtree";
  import { selectionInSecondaryView } from "$lib/state/selection-in-secondary-view";
  import { selectedItems } from "$lib/state/selected-items";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import MultiHistogram from "$lib/widgets/multi-histogram.svelte";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import Column from "$lib/widgets/column.svelte";
  import ControlButton from "$lib/widgets/control-button.svelte";
  import Row from "$lib/widgets/row.svelte";
  import Toggle from "$lib/widgets/toggle.svelte";
  import { visibleInterestingData } from "$lib/state/visible-data";

  export let width: number;
  export let height: number;

  const interactionFactory = new InteractionFactory(width, height, $quadtree);

  let histogramMode: "selected" | "all" = "all";
  let showDoiValues = true;

  $: items = histogramMode === "all" ? $visibleInterestingData : $selectedItems;
  $: data = items.map(dataItemToRecord);

  function onBrush(event: CustomEvent) {
    const selections: Record<string, [number, number]> = event.detail;
    if (selections === null) {
      return;
    }
    const dims = Object.keys(selections);

    if (dims.length === 0) {
      $selectionInSecondaryView = {};
      return;
    }

    dims.forEach((dim) => {
      const interaction = interactionFactory.createHistogramBrushInteraction(
        dim,
        $dimensions.indexOf(dim),
        selections[dim]
      );
      $interactionLog.add(interaction);
    });

    const recent = $interactionLog.getNRecentSteps(1)[0] as HistogramBrushInteraction;

    const dim = recent.dimension;
    $selectionInSecondaryView = {};
    $selectionInSecondaryView[dim] = recent.extent
    // $selectionInSecondaryView = data
    //   .filter((item) => item[dim] >= recent.extent[0] && item[dim] <= recent.extent[1])
    //   .map((item) => item["__item__"] as DataItem);
  }
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

      <Toggle id="doi-values" style="margin-right:10px" bind:active={showDoiValues}>
        show DOI histogram
      </Toggle>
      <!-- <Toggle id="doi-labels" bind:active={showDoiLabels}>doi labels</Toggle> -->
    </Row>
    <ControlButton on:click={() => ($isSecondaryViewCollapsed = true)}>close</ControlButton>
  </Row>
  <Row id="selected-data-histograms" style="width:{width}px">
    <MultiHistogram
      id="secondary-selected-dims"
      {data}
      brushedInterval={$selectionInSecondaryView}
      dimensions={$selectedDoiDimensions.concat(showDoiValues ? ["doi"] : [])}
      showTitle={false}
      groupDimension="selected"
      width={310}
      height={height * 0.4}
      on:end={onBrush}
    />
  </Row>
</Column>

<style>
  :global(#secondary-view) {
    overflow: hidden;
    justify-content: space-between;
    flex-wrap: nowrap;
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
