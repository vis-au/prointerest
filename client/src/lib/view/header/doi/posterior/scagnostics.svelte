<script lang="typescript">
import { scagnosticWeights, selectedScagnostics } from "$lib/state/selected-scagnostics";
import { scagnostics } from "$lib/types/scagnostics";
import type { Scagnostic } from "$lib/types/scagnostics";
import DoiConfig from "$lib/widgets/doi-config.svelte";
import WeightedValues from "$lib/widgets/weighted-values.svelte";
import Column from "$lib/widgets/column.svelte";

export let maxWidth: number;

let selectedWeights = new Map<Scagnostic, number>();


function udpateSelected() {
  const newWeights = new Map<Scagnostic, number>();

  $selectedScagnostics.forEach(scagnostic => {
    newWeights.set(scagnostic, $scagnosticWeights.get(scagnostic));
  });

  selectedWeights = newWeights;
}

function toggleScagnostic(scagnostic: Scagnostic) {
  const index = $selectedScagnostics.indexOf(scagnostic);

  if (index > -1) {
    // reactive slice
    $selectedScagnostics.splice(index, 1);
    const leftHalf = $selectedScagnostics.slice(0, index);
    const rightHalf = $selectedScagnostics.slice(index, $selectedScagnostics.length);
    $selectedScagnostics = leftHalf.concat(rightHalf);
  } else {
    // reactive push
    $selectedScagnostics = [...$selectedScagnostics, scagnostic];
  }

  udpateSelected();
}

udpateSelected();
</script>


<DoiConfig title="Configure Scagnostics">
  <Column>
    <h3 style="margin-top:0;">Select interesting scagnostics</h3>
    <div class="scagnostic-checklist" style="max-width:{maxWidth}px">
      { #each scagnostics as scagnostic }
        <div class="item">
          <input
            id={ scagnostic }
            type="checkbox"
            value={ scagnostic }
            checked={ $selectedScagnostics.indexOf(scagnostic) > -1 }
            on:click={ () => toggleScagnostic(scagnostic) } />
          <label for={ scagnostic }>{ scagnostic }</label>
        </div>
      { /each }
    </div>
  </Column>

  <Column>
    <h3>Assign weights</h3>
    <WeightedValues
      group="selected-scagnostics"
      valueWeights={ selectedWeights }
      totalSize={ maxWidth }
    />
  </Column>
</DoiConfig>


<style>
  div.scagnostic-checklist {
    display: flex;
    flex-flow: row wrap;
    line-height: 30px;
  }
  div.scagnostic-checklist div.item {
    margin-right: 15px;
  }
  div.scagnostic-checklist div.item input {
    display: none;
  }
  div.scagnostic-checklist div.item label {
    background: #efefef;
    cursor: pointer;
    border-radius: 4px;
    padding: 3px 10px;
  }
  div.scagnostic-checklist div.item input:checked+label {
    background: black;
    color: white;
  }
</style>