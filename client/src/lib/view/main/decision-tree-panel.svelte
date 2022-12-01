<script lang="ts">
  import {activeDecisionTree} from "$lib/state/active-decision-tree";
  import {activeFDLTree} from "$lib/state/active-fdl-tree";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import JsObjectViewer from "$lib/widgets/js-object-viewer.svelte";
  import ControlButton from "../../widgets/control-button.svelte";
  import DecisionTreeViewer from "./decision-tree-viewer.svelte";

  export let x = 0;
  export let y = 0;
  export let width = 1000;
  export let height = 500;

  let isHidden = true;  // flag for whether the tree is visible or not
  let showRaw = false;  // flag for showing the JSON viewer of the tree
  let currentlyShownTree = "decision tree";

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
        <div class="left">
          Show
          <Alternatives
            name="currently-shown-tree"
            alternatives={["decision tree", "FDL tree"]}

            bind:activeAlternative={currentlyShownTree}
          />
        </div>

        <div class="right">
          <ControlButton
            on:click={hide}
            style="width:20px;height:20px;line-height:20px;padding:0">
            <div style="transform:rotate(45deg)">+</div>
          </ControlButton>
        </div>
      </h2>

      <DecisionTreeViewer
        id="tree-viewer"
        decisionTree={currentlyShownTree === "decision tree" ? $activeDecisionTree: $activeFDLTree}
      />

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
    font-weight: normal;
    line-height: 1;
    margin: 0;
    margin-bottom: 15px;
    padding: 0;
    justify-content: space-between;
    align-items: center;
  }
  .decision-tree-panel h2 div.left,
  .decision-tree-panel h2 div.right {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
  }
  .decision-tree-panel h2 div.left {
    margin-right: 25px;
  }
  .decision-tree-panel .container {
    background: white;
    border: 1px solid #e8eaed;
    box-shadow: 0 1px 3px -2px #aaa;
    border-radius: 4px;
    padding: 1rem;
  }
</style>
