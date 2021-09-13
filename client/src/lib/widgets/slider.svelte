<script lang="typescript">
  import BigNumber from "./big-number.svelte";

  export let id: string;
  export let label: string;
  export let width: number;
  export let min: number;
  export let max: number;
  export let steps = 100;
  export let value: number;
  export let updateLive = true;
  export let showValue = true;
  export let showDomain = true;
  export let style = "";

  const step = (max - min) / steps;

  let sliderValue = value;
</script>

<div class="slider" style="width:{width}px;{style}">
  <label class="before" for="{id}-slider">{label}</label>
  {#if showValue}
    {#if updateLive}
      <BigNumber style="margin:0 10px 0 5px;width:60px">{value}</BigNumber>
    {:else}
      <BigNumber style="margin:0 10px 0 5px;width:60px">{sliderValue}</BigNumber>
    {/if}
  {/if}
  {#if showDomain}
    <label class="min" for="{id}-slider">{min}</label>
  {/if}
  {#if updateLive}
    <input type="range" id="{id}-slider" {min} {max} {step} bind:value />
  {:else}
    <input
      type="range"
      id="{id}-slider"
      {min}
      {max}
      {step}
      bind:value={sliderValue}
      on:mouseup={() => (value = sliderValue)}
    />
  {/if}
  {#if showDomain}
    <label class="max" for="{id}-slider">{max}</label>
  {/if}
</div>

<style>
  div.slider {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.3);
  }
  div.slider label.min,
  div.slider label.max {
    margin: 0 5px;
  }
  div.slider label.before {
    white-space: nowrap;
  }
  div.slider input {
    -webkit-appearance: none;
    width: 100%;
  }
  div.slider input:focus {
    outline: none;
  }
  div.slider input::-webkit-slider-runnable-track {
    width: 100%;
    height: 3px;
    cursor: pointer;
    background: #fff;
    border-radius: 1.3px;
    border: 1px solid black;
  }
  div.slider input::-webkit-slider-thumb {
    border: 1px solid #000000;
    height: 15px;
    width: 15px;
    border-radius: 15px;
    background: black;
    cursor: pointer;
    -webkit-appearance: none;
    margin-top: -7px;
  }
  div.slider input:focus::-webkit-slider-runnable-track {
    background: #fff;
  }
  div.slider input::-moz-range-track {
    width: 100%;
    height: 3px;
    cursor: pointer;
    background: #fff;
    border-radius: 1.3px;
    border: 1px solid black;
  }
  div.slider input::-moz-range-thumb {
    border: 1px solid #000000;
    height: 15px;
    width: 15px;
    border-radius: 15px;
    background: black;
    cursor: pointer;
  }
</style>
