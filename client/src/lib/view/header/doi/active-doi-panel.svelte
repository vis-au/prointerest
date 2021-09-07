<script>
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
  import Outlierness from "./prior/outlierness.svelte";
  import Dimensions from "./prior/dimensions.svelte";
  import Selection from "./prior/selection.svelte";
  import Provenance from "./posterior/provenance.svelte";
  import Scagnostics from "./posterior/scagnostics.svelte";
</script>

<div class="active-doi-panel">
  <div class="active-doi-panel-container">
    {#if $selectedDoiWeight === "outlierness"}
      <Outlierness />
    {:else if $selectedDoiWeight === "dimensions"}
      <Dimensions />
    {:else if $selectedDoiWeight === "selection"}
      <Selection />
    {:else if $selectedDoiWeight === "scagnostics"}
      <Scagnostics maxWidth={400} />
    {:else if $selectedDoiWeight === "provenance"}
      <Provenance />
    {/if}
  </div>
</div>

<style>
  div.active-doi-panel {
    position: absolute;
    right: 10px;
    top: 100px;
  }
</style>
