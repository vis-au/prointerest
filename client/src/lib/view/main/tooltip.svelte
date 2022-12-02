<script lang="ts">
  import { activeViewMode } from "$lib/state/active-view-mode";
  import { hoveredItems } from "$lib/state/hovered-items";
  import { hoveredScreenPosition } from "$lib/state/hovered-position";
  import { separateThousands, truncateFloat } from "$lib/util/number-transform";
  import Row from "$lib/widgets/row.svelte";

  let innerWidth: number;
  let innerHeight: number;
  let tooltipHeight: number;
  let tooltipWidth: number;

  const padding = 25;

  $: left = Math.max(
    padding,
    Math.min($hoveredScreenPosition[0] + 20, innerWidth - tooltipWidth - padding)
  );
  $: top =
    tooltipHeight / 2 +
    Math.max(padding, Math.min($hoveredScreenPosition[1], innerHeight - tooltipHeight - padding));

  $: selectedCount = $hoveredItems.filter(item => item.selected).length;
  $: selectedPercentage = truncateFloat((selectedCount / $hoveredItems.length) * 100);
</script>

<div
  class="tooltip {$hoveredItems.length === 0 || $activeViewMode === 'scatter' ? 'hidden' : ''}"
  bind:clientHeight={tooltipHeight}
  bind:clientWidth={tooltipWidth}
  style="left:{left}px;top:{top}px"
>
  <Row>
    <span>count: </span>
    <strong>{separateThousands($hoveredItems.length)}</strong>
  </Row>
  {#if selectedCount > 0}
    <Row>
      <span>selected: </span>
      <strong>{selectedCount} ({selectedPercentage}%)</strong>
    </Row>
  {/if}
</div>

<svelte:window bind:innerWidth bind:innerHeight />

<style>
  div.tooltip {
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    padding: 10px 15px;
  }
  div.tooltip.hidden {
    display: none;
  }
</style>
