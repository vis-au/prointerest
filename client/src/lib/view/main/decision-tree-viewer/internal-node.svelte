<script lang="ts">
  import type { DecisionTree } from "$lib/types/decision-tree";
  import { truncateFloat } from "$lib/util/number-transform";
  import LeafNode from "./leaf-node.svelte";

  export let node: DecisionTree

  $: threshold = node.type === "leaf" ? null : truncateFloat(node.threshold, 3);
</script>

<div class="node {node.type}">

  {#if node.type === "internal"}
    <span style="float: left;font-size:50%;margin-right:5px">L</span>
    <span class="feature">{node.feature}</span>

    <div class="options">
      <div class="left">
        <span class="decision">&lt; {threshold}:</span>
        <svelte:self node={node.left} />
      </div>
      <div class="right">
        <span class="decision">&gt;= {threshold}:</span>
        <svelte:self node={node.right} />
      </div>
    </div>
  {:else}
    <LeafNode leaf={node} />
  {/if}
</div>

<style>
  .node {
    padding: 0;
    margin: 0;
    display: inline-block;
  }

  .node.internal {
    /* background: rgba(0, 0, 0, 0.05); */
    display: flex;
    flex-direction: row;
    margin: 5px 0 0;
    margin-left: 5px;
  }
  .node.internal .feature {
    /* font-style: italic; */
    font-family: 'Courier New', Courier, monospace;
  }
  .node.internal .options {
    display: flex;
    flex-direction: column;
    margin-left: 5px;
  }
  .node.internal .options .right {
    margin-top: 10px;
  }

</style>