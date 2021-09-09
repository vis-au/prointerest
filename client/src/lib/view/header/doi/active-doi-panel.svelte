<script lang="typescript">
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
  import Outlierness from "./prior/outlierness.svelte";
  import Dimensions from "./prior/dimensions.svelte";
  import Selection from "./prior/selection.svelte";
  import Provenance from "./posterior/provenance.svelte";
  import Scagnostics from "./posterior/scagnostics.svelte";

  export let width: number;
  export let height: number;
  export let x: number;
  export let y: number;

  $: display = `display:${$selectedDoiWeight === null ? "none" : "flex"}`;
</script>

<div class="active-doi-panel-container" style="{display};width:{width}px;height:{height}px;left:{x}px;top:{y}px" on:click={ () => $selectedDoiWeight = null }>
  <div class="active-doi-panel" on:click={ (event) => event.stopPropagation() }>
    {#if $selectedDoiWeight === "outlierness"}
      <Outlierness />
    {:else if $selectedDoiWeight === "dimensions"}
      <Dimensions />
    {:else if $selectedDoiWeight === "selection"}
      <Selection />
    {:else if $selectedDoiWeight === "scagnostics"}
      <Scagnostics />
    {:else if $selectedDoiWeight === "provenance"}
      <Provenance />
    {/if}
  </div>
</div>

<style>
  div.active-doi-panel-container {
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
  div.active-doi-panel {
    min-width: 700px;
  }
</style>
