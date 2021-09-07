<script lang="typescript">
  import Column from "$lib/widgets/column.svelte";
  import ControlButton from "./control-button.svelte";

  export let isCollapsed: boolean;
</script>

<Column id="split-view">
  <div class="top">
    {#if isCollapsed}
      <ControlButton id="open-button" on:click={() => isCollapsed = false }>open</ControlButton>
    {/if}
    <slot name="top"></slot>
  </div>
  {#if !isCollapsed}
    <div class="bottom">
      <slot name="bottom"></slot>
    </div>
  {/if}
</Column>

<style>
  :global(#open-button) {
    position: absolute;
    bottom: 10px;
    right: 20px;
    z-index: 1000;
  }
  div.top {
    flex-grow: 8
  }
  div.bottom {
    flex-grow: 2;
  }
</style>