<script lang="ts">
  import {activeDecisionTree} from "$lib/state/active-decision-tree";
  import JsObjectViewer from "$lib/widgets/js-object-viewer.svelte";
  import ControlButton from "../../widgets/control-button.svelte";

  export let title = "Hierarchy";
  export let x = 0;
  export let y = 0;
  export let width = 1000;
  export let height = 500;

  let isHidden = false;

  function hide() {
    isHidden = true;
  }

  function show() {
    isHidden = false;
  }
</script>


<div class="hierarchy-viewer" style="left:{x}px;top:{y}px;">
  {#if isHidden}
    <ControlButton style="width:2rem;height:2rem" on:click={show}>DT</ControlButton>
  {:else}
    <JsObjectViewer
      {title}
      {width}
      {height}
      input={$activeDecisionTree}
      style="font-size:14px"
      on:close={hide} />
  {/if}
</div>

<style>
  .hierarchy-viewer {
    position: absolute;
  }
</style>