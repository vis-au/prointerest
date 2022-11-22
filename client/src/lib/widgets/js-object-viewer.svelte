<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import ControlButton from "./control-button.svelte";

  export let title = "Hierarchy";
  export let input: Record<string, unknown> | Record<string, unknown>[];
  export let style = "";


  const dispatch = createEventDispatcher();

  function close() {
    dispatch("close");
  }
</script>


<div class="js-object-viewer" {style}>
  <h2>
    <span>{title}</span>
    <ControlButton on:click={close} style="padding:0.05rem 0.3rem">x</ControlButton>
  </h2>
  <pre>{ JSON.stringify(input, null, 4) }</pre>
</div>

<style>
  .js-object-viewer {
    background: white;
    border: 1px solid #e8eaed;
    box-shadow: 0 1px 3px -2px #aaa;
    border-radius: 4px;
    padding: 1rem;

  }
  .js-object-viewer h2 {
    display: flex;
    font-size: 14px;
    line-height: 1;
    margin: 0;
    padding: 0;
    justify-content: space-between;
  }
  .js-object-viewer pre {
    border: 1px solid #e8eaed;
    padding: 0;
    margin: 0;
    margin-top: 0.5rem;
    line-height: 150%;
    overflow: auto;
  }
</style>