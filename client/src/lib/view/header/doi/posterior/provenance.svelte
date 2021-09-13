<script lang="typescript">
  import { interactionWeights } from "$lib/state/interaction-technique-weights";
  import Column from "$lib/widgets/column.svelte";
  import DoiConfig from "$lib/view/header/doi/doi-panel.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import { exploredItemInterest, exploredItems, interactionThreshold, provenanceLog, provenanceLogSize } from "$lib/state/explored-items";
  import Row from "$lib/widgets/row.svelte";
  import BigNumber from "$lib/widgets/big-number.svelte";
  import Slider from "$lib/widgets/slider.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import type DataItem from "$lib/types/data-item";
  import { separateThousands } from "$lib/util/number-transform";
  import List from "$lib/widgets/list.svelte";

  // TODO: suggest similar/dissimlar data based on prior/posterior/both

  $: provenanceInterestValues = exploredItemsToRecord($exploredItemInterest);
  $: console.log(provenanceInterestValues);
  $: consideredLog = $provenanceLog.log
    .slice($provenanceLog.log.length - $provenanceLogSize, $provenanceLog.log.length)
    .map(d => d.mode)
    .reverse();

  function exploredItemsToRecord(items: Map<DataItem, number>): Record<"interest", number>[] {
    return Array.from(items.values()).map(value => {
      return {"interest": value}
    });
  }

  const histogramSize = 700;
</script>

<DoiConfig
  title="Configure Provenance"
  message="Configure how much weight each interaction should be assigned to, when computing the data of interest."
>
  <Column>
    <h3>Assign weights to interactions</h3>
    <Row style="height:50px;align-items:stretch;margin:20px 0">
      <WeightedValues
        group="interaction-technique-weights"
        totalSize={histogramSize}
        bind:valueWeights={$interactionWeights}
      />
    </Row>

    <Column style="margin: 30px 0;width:{histogramSize - 20}px">
      <h3>
        <span>Interest Distrubtion</span>
        <span style="font-weight:normal">
          Explored: <BigNumber>{separateThousands($exploredItems.length)}</BigNumber>
        </span>
      </h3>
      <Histogram
        id="explored-data-interest"
        data={provenanceInterestValues}
        dimension={"interest"}
        bins={20}
        width={histogramSize - 50}
        height={100}
      />
      <Slider
        id="interest-threshold"
        label="Threshold"
        width={histogramSize}
        min={0}
        max={1}
        updateLive={false}
        style="margin-top: 20px"
        bind:value={$interactionThreshold}
      />
    </Column>

    <Column>
      <h3>Provenance Log (newest first)</h3>
      <List values={consideredLog} isOrdered={true} style="width:{histogramSize}px" />
      <Row style="margin:20px 0">
        <Slider
          id="log-size"
          label="Log size"
          width={histogramSize}
          min={1}
          max={100}
          steps={99}
          updateLive={false}
          style="margin-top: 20px"
          bind:value={$provenanceLogSize}
        />
      </Row>
    </Column>
  </Column>
</DoiConfig>

<style>
  h3 {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    font-size: 12pt;
    margin: 10px 0;
  }
</style>
