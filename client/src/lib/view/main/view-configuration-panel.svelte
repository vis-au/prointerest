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
    style="padding:5px 10px;margin-right:10px;"
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
    border-left: 2px solid black;
    flex-direction: row;
    align-items: center;
    padding: 0 5px;
    border-left: 1px solid black;
    border-right: 1px solid black;
  }
</style>