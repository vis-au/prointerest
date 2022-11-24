<script lang="ts">
  import type {LeafNode} from "$lib/types/decision-tree";

  export let leaf: LeafNode;
</script>

<div class="leaf">
  <span class="value">{JSON.stringify(leaf.value[0])}</span>
</div>

<style>
  div.leaf {
    margin-left: 5px;
  }
  div.leaf .value {
    padding: 1px 10px;
    border: 1px solid #ccc;
  }
</style>
