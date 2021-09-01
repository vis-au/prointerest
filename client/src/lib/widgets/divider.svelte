<script lang="typescript">
import type { ResizeEvent } from "$lib/types/resize-event";

  import { createEventDispatcher } from "svelte";

  export let group: string;
  export let left: string;
  export let right: string;
  export let isResizing = false;

  const dispatch = createEventDispatcher();

  function resizeStart(x, y) {
    dispatch("resize-started", {
      group,
      startX: x,
      startY: y,
      leftId: left,
      rightId: right
    } as ResizeEvent);
  }
</script>

<div
  class="divider {isResizing ? "active" : ""}"
  on:mousedown={ (e) => resizeStart(e.screenX, e.screenY) }
/>

<style>
	div.divider {
		min-width: 0.5rem;
		min-height: 12px;
		cursor: w-resize;
	}
	div.divider:hover {
		background: #ccc;
	}
  div.divider.active {
    background: steelblue;
  }
</style>