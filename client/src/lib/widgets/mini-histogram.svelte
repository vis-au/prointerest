<script lang="ts">
  import { max, scaleLinear } from "d3";

  export let id: string;
  export let width = 100;
  export let height = 20;
  export let domain: [number, number] = null;
  export let values: number[];
  export let binStyle = "";
  export let histogramStyle = "";

  $: scaleX = scaleLinear()
    .domain(domain ? domain : [0, max(values)])
    .range([0, height]);
</script>

<div
  {id}
  class="mini-histogram"
  style:width="{width}px"
  style:height="{height}px"
  style={histogramStyle}
>
  {#each values as value}
    <div
      class="bin"
      style={binStyle}
      style:width="{width / values.length}px"
      style:height="{scaleX(value)}px"
      title={value.toString()}
    />
  {/each}
</div>

<style>
  div.mini-histogram {
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: flex-end;
    background: #efefef;
  }
  div.mini-histogram .bin {
    box-sizing: border-box;
    border: 0.5px solid #888;
    background: white;
  }
  div.mini-histogram .bin:hover {
    opacity: 0.73;
  }
</style>
