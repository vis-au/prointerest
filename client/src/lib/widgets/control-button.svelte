<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let id = "";
  export let className = "";
  export let mode: "dark" | "light" = "dark";
  export let style = "";

  const dispatch = createEventDispatcher();

  function click() {
    dispatch("click");
  }
</script>

<button {id} class="control-button {mode} {className}" on:click={click} {style}>
  <slot />
</button>

<style>
  button.control-button {
    cursor: pointer;
    border-radius: 3px;
    font-size: 12pt;
    transition: ease-in 0.05s;
  }
  button.control-button:hover {
    background: #aaa;
  }
  button.control-button.dark {
    background: #333;
    color: white;
    border: none;
  }
  button.control-button.light {
    background: white;
    color: black;
    border: 1px solid black;
  }
</style>
