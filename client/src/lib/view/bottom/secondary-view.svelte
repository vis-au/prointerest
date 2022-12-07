<script lang="ts">
  import InteractionFactory from "$lib/provenance/doi-interaction-factory";
  import type HistogramBrushInteraction from "$lib/provenance/histogram-brush-interaction";
  import { interactionLog } from "$lib/provenance/interaction-log";
  import { getRGB, HIGHLIGHT_COLOR, PRIMARY_COLOR } from "$lib/state/active-view-encodings";
  import { doiLimit } from "$lib/state/doi-limit";
  import { selectedDoiDimensions } from "$lib/state/interesting-dimensions";
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { items } from "$lib/state/items";
  import { dimensions } from "$lib/state/processed-data";
  import { quadtree } from "$lib/state/quadtree";
  import { selectedItems } from "$lib/state/selected-items";
  import { selectionInSecondaryView } from "$lib/state/selection-in-secondary-view";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import Column from "$lib/widgets/column.svelte";
  import ControlButton from "$lib/widgets/control-button.svelte";
  import MultiHistogram from "$lib/widgets/multi-histogram.svelte";
  import Row from "$lib/widgets/row.svelte";
  import Toggle from "$lib/widgets/toggle.svelte";

  export let width: number;
  export let height: number;

  const interactionFactory = new InteractionFactory(width, height, $quadtree);

  let histogramMode: "stack interest in selection" | "stack selected" | "stack interesting" =
    "stack interesting";
  let showDoiValues = true;

  $: _items = histogramMode === "stack interest in selection" ? $selectedItems : $items;
  $: data = _items.map(dataItemToRecord);

  $: transform =
    ["stack interesting", "stack interest in selection"].indexOf(histogramMode) > -1
      ? [{ calculate: `datum.doi >= ${$doiLimit}`, as: "interesting" }]
      : null;

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
    $selectionInSecondaryView[dim] = recent.extent;
  }
</script>

<Column id="secondary-view" {width} {height}>
  <Row id="secondary-header" style="margin-bottom: 5px">
    <Row>
      <Row style="margin-right:20px;padding-bottom:3px">
        <h2>Mode:</h2>
        <Alternatives
          name="active-histogram-mode"
          alternatives={["stack interesting", "stack selected", "stack interest in selection"]}
          bind:activeAlternative={histogramMode}
        />
      </Row>

      <Toggle id="doi-values" style="margin-right:10px" bind:active={showDoiValues}>
        show DOI histogram
      </Toggle>
    </Row>
    <ControlButton on:click={() => ($isSecondaryViewCollapsed = true)}>close</ControlButton>
  </Row>
  <Row id="selected-data-histograms" style="width:{width}px">
    <Column>
      <div class="colors">
        <div class="interesting color">
          <div class="legend" style:background={getRGB(PRIMARY_COLOR)} />
          <span class="label">
            {histogramMode === "stack selected" ? "selected" : "interesting"}
          </span>
        </div>
        <div class="uninteresting color">
          <div class="legend" style:background={getRGB(HIGHLIGHT_COLOR)} />
          <span class="label">
            {histogramMode === "stack selected" ? "not selected" : "uninteresting"}
          </span>
        </div>
      </div>
      <MultiHistogram
        id="secondary-selected-dims"
        {data}
        {transform}
        brushedInterval={$selectionInSecondaryView}
        dimensions={$selectedDoiDimensions.concat(showDoiValues ? ["doi"] : [])}
        showTitle={false}
        groupDimension={histogramMode === "stack selected" ? "selected" : "interesting"}
        colors={[getRGB(HIGHLIGHT_COLOR), getRGB(PRIMARY_COLOR)]}
        width={310}
        height={height * 0.4}
        on:end={onBrush}
      />
    </Column>
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

  div.colors {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    font-size: 12px;
    margin: 10px 0;
  }
  div.colors div.color {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    margin: 0 5px;
  }
  div.colors div.color .legend {
    width: 10px;
    height: 10px;
    margin: 0 5px;
  }
</style>
