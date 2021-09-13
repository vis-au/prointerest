<script lang="typescript">
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
    margin: 0 5px;
    cursor: pointer;
  }
  label.toggle input {
    display: none;
  }
  label.toggle span {
    background: #efefef;
    color: #000;
    padding: 3px 10px;
    border-radius: 3px;
    -moz-user-select: none;
    -webkit-user-select: none;
  }
  label.toggle input:checked + span {
    background: #555;
    color: #fff;
  }
</style>
