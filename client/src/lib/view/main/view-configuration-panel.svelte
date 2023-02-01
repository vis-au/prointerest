<script lang="ts">
  import ControlButton from "$lib/widgets/control-button.svelte";

  export let label = "";
  export let active = false;

  function toggle() {
    active = !active;
  }
</script>

<div class="configuration" class:active>
  <div class="controls">
    {#if active}
      <slot />
    {/if}
  </div>
  <ControlButton on:click={toggle} style="width: 100%;font-size:12px;height:auto;padding:5px 10px;margin-top:5px">
    {label}
  </ControlButton>
</div>

<style>
  div.configuration {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border: 1px solid #ddd;
    padding: 2px 5px;
    margin: 0 5px;
    border-radius: 4px;
  }
  div.configuration div.controls {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 30px;
  }
</style>