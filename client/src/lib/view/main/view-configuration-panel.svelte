<script lang="ts">
  import ControlButton from "$lib/widgets/control-button.svelte";

  export let label = "";
  export let active = false;

  function toggle() {
    active = !active;
  }
</script>

<div class="configuration" class:active>
  <ControlButton
    on:click={toggle}
    mode={active ? "dark" : "light"}
    style="padding:5px 10px;"
  >
    {label}
  </ControlButton>

  {#if active}
    <slot />
  {/if}
</div>

<style>
  div.configuration {
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid #ddd;
    padding: 2px 5px;
    margin: 0 5px;
    border-radius: 4px;
  }
</style>