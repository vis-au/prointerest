<script lang="typescript">
  import Column from "$lib/widgets/column.svelte";

  export let isCollapsed: boolean;
</script>

<Column id="split-view">
  <div class="top">
    <slot name="top"></slot>
  </div>
  {#if !isCollapsed}
    <div class="bottom">
      <slot name="bottom"></slot>
    </div>
  {/if}
</Column>

<style>
  div.top {
    flex-grow: 8
  }
  div.bottom {
    flex-grow: 2;
  }
</style>