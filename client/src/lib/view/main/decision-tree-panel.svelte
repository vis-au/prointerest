<script lang="ts">
  import {activeDecisionTree} from "$lib/state/active-decision-tree";
  import JsObjectViewer from "$lib/widgets/js-object-viewer.svelte";
  import ControlButton from "../../widgets/control-button.svelte";
  import DecisionTreeViewer from "./decision-tree-viewer/decision-tree-viewer.svelte";

  export let title = "Decision Tree";
  export let x = 0;
  export let y = 0;
  export let width = 1000;
  export let height = 500;

  let isHidden = false;
  let showRaw = false;

  function hide() {
    isHidden = true;
  }

  function show() {
    isHidden = false;
  }
</script>


<div class="decision-tree-panel" style="left:{x}px;top:{y}px;">
  {#if isHidden}
    <ControlButton style="width:2rem;height:2rem" on:click={show}>DT</ControlButton>
  {:else}

    <div class="container">
      <h2>
        <span style="margin-right:10px">{title}</span>
        <ControlButton
          on:click={hide}
          style="width:20px;height:20px;line-height:20px;padding:0">
          <div style="transform:rotate(45deg)">+</div>
        </ControlButton>
      </h2>

      <DecisionTreeViewer tree={$activeDecisionTree}/>

      {#if showRaw}
        <JsObjectViewer
          {width}
          {height}
          input={$activeDecisionTree}
          style="font-size:14px"
          on:close={hide} />
      {/if}
    </div>
  {/if}
</div>

<style>
  .decision-tree-panel {
    position: absolute;
    font-size: 12px;
  }
  .decision-tree-panel h2 {
    display: flex;
    font-size: 14px;
    line-height: 1;
    margin: 0;
    padding: 0;
    justify-content: space-between;
    align-items: center;
  }
  .decision-tree-panel .container {
    background: white;
    border: 1px solid #e8eaed;
    box-shadow: 0 1px 3px -2px #aaa;
    border-radius: 4px;
    padding: 1rem;
  }
</style>
