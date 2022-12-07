<script lang="ts">
  import { exploredItemInterest, exploredItems } from "$lib/state/explored-items";
  import type DataItem from "$lib/types/data-item";
  import DoiConfig from "$lib/view/header/doi/doi-panel.svelte";
  import Column from "$lib/widgets/column.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import Row from "$lib/widgets/row.svelte";
  import BigNumber from "$lib/widgets/big-number.svelte";
  import Slider from "$lib/widgets/slider.svelte";
  import Histogram from "$lib/widgets/histogram.svelte";
  import List from "$lib/widgets/list.svelte";
  import Toggle from "$lib/widgets/toggle.svelte";
  import { randomDataSample } from "$lib/state/sampled-data";
  import { interactionLog } from "$lib/provenance/interaction-log";
  import { sendProvenanceConfig, sendProvenanceWeights } from "$lib/util/requests";
  import { interactionWeights } from "$lib/state/active-doi-weights";

  let provenanceSize = 100;
  let interactionThreshold = 0.15;

  $: provenanceInterestValues = exploredItemsToRecord($exploredItemInterest);
  $: start = Math.max($interactionLog.log.length - provenanceSize, 0);
  $: consideredLog = $interactionLog.log
    .slice(start, $interactionLog.log.length)
    .map((d) => d.mode)
    .reverse();

  $: percentage = Math.floor(($exploredItems.length / $randomDataSample.length) * 10000) / 100;

  function exploredItemsToRecord(items: Map<DataItem, number>): Record<"interest", number>[] {
    return Array.from(items.values()).map((value) => {
      return { interest: value };
    });
  }

  const histogramSize = 700;
  let showAggregateInteractionCount = true;
  let autoUpdateAfterWeights = false;
</script>

<DoiConfig
  title="Configure Provenance"
  message="Configure how much weight each interaction should be assigned to, when computing the data of interest."
>
  <Column>
    <h3 style:width="{histogramSize - 20}px">
      Assign weights to interactions
      <Toggle id="auto-update" style="font-weight:normal" bind:active={autoUpdateAfterWeights}>
        auto update
      </Toggle>
    </h3>
    <Row style="height:50px;align-items:stretch;margin:20px 0">
      <WeightedValues
        id="interaction-technique-weights"
        totalSize={histogramSize}
        bind:valueWeights={$interactionWeights}
        on:end={() => {
          sendProvenanceWeights($interactionWeights);
        }}
      />
    </Row>

    <Column style="margin: 30px 0;width:{histogramSize - 20}px">
      <h3>
        <span>Interest Distrubtion</span>
        <span style="font-weight:normal">
          Explored: <BigNumber>~{percentage}%</BigNumber>
        </span>
      </h3>
      <Histogram
        id="explored-data-interest"
        data={provenanceInterestValues}
        dimension={"interest"}
        bins={20}
        domain={[0, 1]}
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
        bind:value={interactionThreshold}
        on:end={() => sendProvenanceConfig({ threshold: interactionThreshold })}
      />
    </Column>

    <Column style="width:{histogramSize - 20}px">
      <h3>
        <span>Provenance Log (newest first)</span>
        <Toggle style="font-weight:normal" bind:active={showAggregateInteractionCount}>
          summerize
        </Toggle>
      </h3>
      <List
        values={consideredLog}
        isOrdered={true}
        count={showAggregateInteractionCount}
        style="width:{histogramSize}px"
      />
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
          bind:value={provenanceSize}
          on:end={() => sendProvenanceConfig({ log_size: provenanceSize })}
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
    align-items: center;
    font-size: 12pt;
    margin: 10px 0;
  }
</style>
