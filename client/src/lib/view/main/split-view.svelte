<script lang="ts">
  import { selectionInSecondaryView } from "$lib/state/selection-in-secondary-view";
  import Column from "$lib/widgets/column.svelte";
  import ControlButton from "../../widgets/control-button.svelte";

  export let isCollapsed: boolean;
</script>

<Column id="split-view">
  <div class="top">
    {#if isCollapsed}
      <ControlButton
        id="open-button"
        on:click={() => (isCollapsed = false)}
        style="border:1px solid {Object.keys($selectionInSecondaryView).length > 0
          ? 'orange'
          : 'black'}"
      >
        open
      </ControlButton>
    {/if}
    <slot name="top" />
  </div>
  {#if !isCollapsed}
    <div class="bottom">
      <slot name="bottom" />
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
    flex-grow: 8;
  }
  div.bottom {
    flex-grow: 2;
  }
</style>
