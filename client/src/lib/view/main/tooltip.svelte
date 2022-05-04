<script lang="ts">
  import { median } from "d3";
  import { activeBinMode } from "$lib/state/active-bin-mode";
  import { activeViewMode } from "$lib/state/active-view-mode";
  import { doiValues } from "$lib/state/doi-values";
  import { hoveredItems } from "$lib/state/hovered-items";
  import { hoveredScreenPosition } from "$lib/state/hovered-position";
  import { separateThousands, truncateFloat } from "$lib/util/number-transform";

  let innerWidth: number;
  let innerHeight: number;
  let tooltipHeight: number;
  let tooltipWidth: number;

  const padding = 25;

  $: left = Math.max(
    padding, Math.min($hoveredScreenPosition[0] + 20, innerWidth - tooltipWidth - padding)
  );
  $: top = tooltipHeight/2 + Math.max(
    padding, Math.min($hoveredScreenPosition[1], innerHeight - tooltipHeight - padding)
  );
</script>

<div class="tooltip {$hoveredItems.length === 0 || $activeViewMode === "scatter" ? "hidden" : ""}"
  bind:clientHeight={tooltipHeight}
  bind:clientWidth={tooltipWidth}
  style="left:{left}px;top:{top}px">

  { #if $activeBinMode === "density" }
    <span>count: </span><strong>{
      separateThousands($hoveredItems.length)
    }</strong>
  { :else }
    <span>median doi: </span><strong>{
       truncateFloat(median($hoveredItems.map(item => +$doiValues.get(item.id))), 3)
    }</strong>
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