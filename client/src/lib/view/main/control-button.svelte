<script lang="typescript">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  function click() {
    dispatch("click")
  }
</script>

<button class="control-button" on:click={ () => click() }>
  <slot></slot>
</button>

<style>
  button.control-button {
    background: #333;
    color: white;
    cursor: pointer;
    border: none;
    border-radius: 3px;
    font-size: 12pt;
  }
</style>