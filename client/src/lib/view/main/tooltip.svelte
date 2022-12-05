<script lang="ts">
  import { activeViewEncodings } from "$lib/state/active-view-encodings";
  import { hoveredItems } from "$lib/state/hovered-items";
  import { hoveredScreenPosition } from "$lib/state/hovered-position";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { separateThousands, truncateFloat } from "$lib/util/number-transform";
  import Row from "$lib/widgets/row.svelte";
  import Column from "$lib/widgets/column.svelte";
  import { currentTransform } from "$lib/state/zoom";

  let innerWidth: number;
  let innerHeight: number;
  let tooltipHeight: number;
  let tooltipWidth: number;

  const padding = 25;

  $: left = Math.max(
    padding,
    Math.min($hoveredScreenPosition[0] + 20, innerWidth - tooltipWidth - padding)
  );
  $: top = Math.max(
    padding,
    Math.min($hoveredScreenPosition[1], innerHeight - tooltipHeight - padding)
  );

  $: selectedCount = $hoveredItems.filter((item) => item.selected).length;
  $: selectedPercentage = truncateFloat((selectedCount / $hoveredItems.length) * 100);
</script>

<div
  class="tooltip"
  bind:clientHeight={tooltipHeight}
  bind:clientWidth={tooltipWidth}
  style="left:{left}px;top:{top}px"
>
  <Column>
    <Row
      >{$activeViewEncodings.x}: {truncateFloat(
        $scaleX.invert($currentTransform.invertX($hoveredScreenPosition[0]))
      )}</Row
    >
    <Row
      >{$activeViewEncodings.y}: {truncateFloat(
        $scaleY.invert($currentTransform.invertY($hoveredScreenPosition[1]))
      )}</Row
    >
  </Column>
  {#if $hoveredItems.length > 0}
    <hr />
    <Row>
      <span>#items: </span>
      <strong>{separateThousands($hoveredItems.length)}</strong>
    </Row>
  {/if}
  {#if selectedCount > 0}
    <Row>
      <span>selected: </span>
      <strong>{separateThousands(selectedCount)} ({selectedPercentage}%)</strong>
    </Row>
  {/if}
</div>

<svelte:window bind:innerWidth bind:innerHeight />

<style>
  div.tooltip {
    user-select: none;
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    padding: 10px 15px;
    font-size: 12px;
  }
  div.tooltip hr {
    height: 0.25px;
    color: #aaa;
  }
</style>
