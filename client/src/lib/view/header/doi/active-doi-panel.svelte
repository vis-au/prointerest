<script lang="typescript">
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
  import Outlierness from "./prior/outlierness.svelte";
  import Dimensions from "./prior/dimensions.svelte";
  import Provenance from "./posterior/provenance.svelte";
  import Scagnostics from "./posterior/scagnostics.svelte";
  import MainViewOverlay from "$lib/widgets/main-view-overlay.svelte";

  export let x: number;
  export let y: number;
  export let width: number;
  export let height: number;

  function close() {
    $selectedDoiWeight = null;
  }
</script>

<MainViewOverlay {x} {y} {width} {height} visible={$selectedDoiWeight !== null} on:close={close}>
  {#if $selectedDoiWeight === "outlierness"}
    <Outlierness />
  {:else if $selectedDoiWeight === "dimensions"}
    <Dimensions />
  {:else if $selectedDoiWeight === "scagnostics"}
    <Scagnostics />
  {:else if $selectedDoiWeight === "provenance"}
    <Provenance />
  {/if}
</MainViewOverlay>
