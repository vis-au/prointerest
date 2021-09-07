<script lang="typescript">
  import { createEventDispatcher } from "svelte";

  import type { ResizeEvent } from "$lib/types/resize-event";

  export let group: string;
  export let left: string;
  export let right: string;
  export let isResizing = false;
  export let weights: Map<string, number>;

  const dispatch = createEventDispatcher();

  function resizeStart(x: number, y: number) {
    dispatch("resize-started", {
      group,
      weights,
      startX: x,
      startY: y,
      leftId: left,
      rightId: right,
      leftValue: 0,
      rightValue: 0
    } as ResizeEvent);
  }
</script>

<div
  class="divider {isResizing ? 'active' : ''}"
  on:mousedown={(e) => resizeStart(e.clientX, e.clientY)}
/>

<style>
  div.divider {
    min-width: 0.5rem;
    min-height: 12px;
    cursor: col-resize;
  }
  div.divider:hover {
    background: #ccc;
  }
  div.divider.active {
    background: #333;
  }
</style>
