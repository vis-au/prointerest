<script lang="ts">
    import type { DecisionTree } from "$lib/types/decision-tree";
    import InternalNode from "./internal-node.svelte";

    export let tree: DecisionTree;
    export let height = 1200;
    export let width = 1000;
    export let style = "";
</script>

<div class="decision-tree-viewer" {style}>
  {#if !tree}
    <span>no dt, yet</span>
  {:else}
    <div class="nodes" style="max-height:{height}px;max-width:{width}px">
      <InternalNode node={tree} />
    </div>
  {/if}
</div>

<style>
  .decision-tree-viewer .nodes {
    border: 1px solid #e8eaed;
    padding: 0;
    margin: 0;
    margin-top: 0.5rem;
    line-height: 150%;
    overflow: auto;
  }
</style>