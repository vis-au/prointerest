<script lang="typescript">
  import { createEventDispatcher } from "svelte";

  export let className = "";
  export let id = "";

  const dispatch = createEventDispatcher();

  function click() {
    dispatch("click")
  }
</script>

<button {id} class="control-button {className}" on:click={ click }>
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