<script lang="typescript">
  import { processedData, totalSize } from "$lib/state/processed-data";
  import {
    pauseProgression,
    progressionState,
    resetProgression,
    startProgression
  } from "$lib/state/progression";
import { abbreviate } from "$lib/util/number-transform";
  import BigNumber from "$lib/widgets/big-number.svelte";
  import Column from "$lib/widgets/column.svelte";
  import ProgressBar from "$lib/widgets/progress-bar.svelte";
  import Row from "$lib/widgets/row.svelte";
  import ControlButton from "./control-button.svelte";

  export let x: number;
  export let y: number;

  const width = 120;

  $: progress = $processedData.length / $totalSize;
</script>

<Row id="progression-controls" style="left:{x}px;top:{y}px">
  <Column>
    <div id="progression-text">
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
  <Row id="buttons">
    {#if $progressionState === "paused"}
      <ControlButton on:click={startProgression}>start</ControlButton>
    {:else if $progressionState === "running"}
      <ControlButton on:click={pauseProgression}>pause</ControlButton>
    {/if}
    <ControlButton on:click={resetProgression}>reset</ControlButton>
  </Row>
</Row>

<style>
  :global(#progression-controls) {
    position: absolute;
    font-size: 10pt;
    background: white;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
  div#progression-text {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  :global(#buttons button) {
    margin-left: 5px;
  }
</style>
