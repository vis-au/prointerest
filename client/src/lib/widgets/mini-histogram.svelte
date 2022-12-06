<script lang="ts">
  import { max, scaleLinear } from "d3";

  export let id: string;
  export let width = 100;
  export let height = 20;
  export let values: number[];
  export let style = "";

  $: scaleX = scaleLinear([0, max(values)], [0, height]);
</script>

<div {id} class="mini-histogram" {style}>
  {#each values as value}
    <div
      class="bin"
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
    align-items: baseline;
  }
  div.mini-histogram .bin {
    box-sizing: border-box;
    border: 1px solid #333;
    background: white;
  }
</style>