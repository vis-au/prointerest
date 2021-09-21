<script lang="typescript">
  import InteractionFactory from "$lib/provenance/doi-interaction-factory";
  import type HistogramBrushInteraction from "$lib/provenance/histogram-brush-interaction";
  import { interactionLog } from "$lib/provenance/interaction-log";
  import { interestingDimensions } from "$lib/state/interesting-dimensions";
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { dimensions } from "$lib/state/processed-data";
  import { randomlySampledBinItems } from "$lib/state/randomly-sampled-items";
  import { quadtree } from "$lib/state/quadtree";
  import { secondaryBrushedItems } from "$lib/state/secondary-brushed-items";
  import { selectedItems } from "$lib/state/selected-items";
  import type DataItem from "$lib/types/data-item";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import MultiHistogram from "$lib/widgets/multi-histogram.svelte";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import Column from "$lib/widgets/column.svelte";
  import ControlButton from "$lib/widgets/control-button.svelte";
  import Options from "$lib/widgets/options.svelte";
  import Row from "$lib/widgets/row.svelte";
  import Toggle from "$lib/widgets/toggle.svelte";

  export let width: number;
  export let height: number;

  const interactionFactory = new InteractionFactory(width, height, $quadtree);

  let histogramMode: "selected" | "all" = "all";
  let showDoiLabels = true;
  let showDoiValues = true;

  $: items = histogramMode === "all" ? $randomlySampledBinItems : $selectedItems;
  $: data = items.map(dataItemToRecord);

  $: selectedDoiDimensions = [showDoiValues ? "doi" : null, showDoiLabels ? "label" : null].filter(
    (d) => d !== null
  );

  $: selectedDimensions = Object.keys($interestingDimensions)
    .filter((d) => $interestingDimensions[d])
    .concat(selectedDoiDimensions);

  function onBrush(event: CustomEvent) {
    const selections: Record<string, [number, number]> = event.detail;
    if (selections === null) {
      return;
    }
    const dims = Object.keys(selections);

    if (dims.length === 0) {
      $secondaryBrushedItems = [];
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

    if (recent.dimension === "doi" || recent.dimension === "label") {
      const dim = recent.dimension;
      $secondaryBrushedItems = data
        .filter((item) => item[dim] >= recent.extent[0] && item[dim] <= recent.extent[1])
        .map((item) => item["__item__"] as DataItem);
    } else {
      $secondaryBrushedItems = recent.getAffectedItems();
    }
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
      <Options
        options={$dimensions}
        showInactive={false}
        bind:activeOptions={$interestingDimensions}
      />
      <Toggle id="doi-values" style="margin-right:10px" bind:active={showDoiValues}
        >doi values</Toggle
      >
      <Toggle id="doi-labels" bind:active={showDoiLabels}>doi labels</Toggle>
    </Row>
    <ControlButton on:click={() => ($isSecondaryViewCollapsed = true)}>close</ControlButton>
  </Row>
  <Row id="selected-data-histograms" style="width:{width}px">
    <MultiHistogram
      id="secondary-selected-dims"
      {data}
      dimensions={selectedDimensions}
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
