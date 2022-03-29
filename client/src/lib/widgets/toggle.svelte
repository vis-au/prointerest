<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let id = "";
  export let active: boolean;
  export let style = "";

  const dispatch = createEventDispatcher();
</script>

<label {id} class="toggle" for="{id}-toggle" {style}>
  <input
    id="{id}-toggle"
    type="checkbox"
    bind:checked={active}
    on:change={() => dispatch("changed", active)}
  />

  <span>
    <slot />
  </span>
</label>

<style>
  label.toggle {
    cursor: pointer;
  }
  label.toggle span {
    -moz-user-select: none;
    -webkit-user-select: none;
  }
</style>
