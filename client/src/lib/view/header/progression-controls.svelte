<script lang="ts">
  import { averageDoiPerChunk } from "$lib/state/doi-values";
  import { processedData, totalSize } from "$lib/state/processed-data";
  import {
    currentChunkNo,
    pauseProgression,
    progressionState,
    resetProgression,
    startProgression
  } from "$lib/state/progression";
  import { abbreviate } from "$lib/util/number-transform";
  import BigNumber from "$lib/widgets/big-number.svelte";
  import Column from "$lib/widgets/column.svelte";
  import MiniHistogram from "$lib/widgets/mini-histogram.svelte";
  import ProgressBar from "$lib/widgets/progress-bar.svelte";
  import Row from "$lib/widgets/row.svelte";
  import ControlButton from "../../widgets/control-button.svelte";

  export let x = 0;
  export let y = 0;
  export let useAbsolutePositioning = true;
  export let useDarkMode = false;
  export let style = "";

  const width = 120;

  $: progress = $processedData.length / $totalSize;
</script>

<div
  class="progression-controls"
  class:dark={useDarkMode}
  style:position={useAbsolutePositioning ? "absolute" : "relative"}
  style:left="{x}px"
  style:top="{y}px"
  {style}
>
  <Row>
    <Row>
      <span>Iteration: <BigNumber>{$currentChunkNo}</BigNumber></span>
      <MiniHistogram
        id="mean-doi-per-chunk"
        domain={[0, 1]}
        width={150}
        height={25}
        values={$averageDoiPerChunk}
        style="padding:0 5px;"
      />
    </Row>
    <Column>
      <div class="progression-text">
        <span>Processed:</span>
        <span><BigNumber>{abbreviate($processedData.length)}</BigNumber></span>
      </div>
      <ProgressBar
        id={"progression"}
        {progress}
        current={$processedData.length}
        total={$totalSize}
        {width}
        height={5}
      />
    </Column>
    <div class="control-panel-buttons" style="display:row;align-items:center;">
      {#if $progressionState === "paused"}
        <ControlButton on:click={startProgression}>start</ControlButton>
      {:else if $progressionState === "running"}
        <ControlButton on:click={pauseProgression}>pause</ControlButton>
      {/if}
      <ControlButton on:click={resetProgression}>reset</ControlButton>
    </div>
  </Row>
</div>

<style>
  .progression-controls {
    color: black;
    font-size: 10pt;
    background: white;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
  .progression-controls.dark {
    color: white;
    background: #333;
    border: none;
    padding: 0 5px;
  }
  .progression-text {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  :global(.progression-controls .control-panel-buttons button) {
    margin-left: 5px;
    width: 50px;
  }
  :global(.progression-controls.dark .control-panel-buttons button) {
    background: #555;
  }
  :global(.progression-controls .big-number) {
    color: #333;
    max-width: 50px;
  }
  :global(.progression-controls.dark .big-number) {
    background: none;
    color: #fff;
    padding: 0;
  }
  :global(.progression-controls.dark .progress-bar) {
    border-color: white;
  }
</style>
