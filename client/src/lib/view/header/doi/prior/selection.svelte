<script lang="typescript">
  import { isSecondaryViewCollapsed } from "$lib/state/is-secondary-view-collapsed";
  import { selectedItems } from "$lib/state/selected-items";
  import ControlButton from "$lib/view/main/control-button.svelte";
  import BigNumber from "$lib/widgets/big-number.svelte";
  import DoiConfig from "$lib/view/header/doi/doi-config.svelte";
</script>

<DoiConfig
  title="Selected Data Items"
  message="Investigate the distributions in the data items selected as interesting using the brush across all dimensions in the data."
>
  <p class="selected">
    <BigNumber>{$selectedItems.length}</BigNumber> items in selections.
  </p>
  {#if $selectedItems.length === 0}
    <p class="message">Hint: No items selected. You can use the brush or select individual bins.</p>
  {/if}
  {#if $isSecondaryViewCollapsed}
    <ControlButton on:click={() => $isSecondaryViewCollapsed=false}>open histograms</ControlButton>
  {:else}
    <ControlButton on:click={() => $isSecondaryViewCollapsed=true}>close histograms</ControlButton>
  {/if}
</DoiConfig>

<style>
  p.selected {
    margin-bottom: 10px;
  }
  p.message {
    color: #999;
  }
</style>
