<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let width: number;
  export let height: number;
  export let x: number;
  export let y: number;
  export let visible: boolean;

  const dispatch = createEventDispatcher();

  $: display = `${visible ? "flex" : "none"}`;
  $: left = `${x}px`;
  $: top = `${y}px`;
  $: w = `${width}px`;
  $: h = `${height}px`;

  function close() {
    dispatch("close");
  }
</script>

<div
  class="main-view-overlay-container"
  style:display
  style:left
  style:top
  style:width={w}
  style:height={h}
  on:click={close}>

  <div class="main-view-overlay" on:click={(event) => event.stopPropagation()}>
    <slot />
  </div>
</div>

<style>
  div.main-view-overlay-container {
    position: absolute;
    left: 0;
    top: 0;
    padding: 70px;
    background: rgba(255, 255, 255, 0.5);
    z-index: 1000;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
  }
  div.main-view-overlay {
    min-width: 700px;
  }
</style>
