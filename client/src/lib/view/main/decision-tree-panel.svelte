<script lang="ts">
  import { activeDecisionTree } from "$lib/state/active-decision-tree";
  import { activeFDLTree } from "$lib/state/active-fdl-tree";
  import { selectedDTNode } from "$lib/state/selection-in-dt";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import DecisionTreeViewer from "./decision-tree-viewer.svelte";
  import ViewPanel from "./view-panel.svelte";

  export let x = 0;
  export let y = 0;
  export let width = 500;
  export let height = 500;

  let currentlyShownTree = "decision tree";

</script>

<ViewPanel label="DT" {x} {y} active={$selectedDTNode !== null}>
  <div class="header" slot="header">
    Show
    <Alternatives
      name="currently-shown-tree"
      alternatives={["decision tree", "FDL tree"]}
      bind:activeAlternative={currentlyShownTree}
    />
  </div>
  <DecisionTreeViewer
    slot="body"
    id="tree-viewer"
    {width}
    {height}
    decisionTree={currentlyShownTree === "decision tree" ? $activeDecisionTree : $activeFDLTree}
  />
</ViewPanel>

<style>
  div.header {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
  }
</style>
