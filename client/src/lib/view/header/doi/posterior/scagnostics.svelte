<script lang="typescript">
  import { scagnosticWeights, selectedScagnostics } from "$lib/state/selected-scagnostics";
  import { scagnostics } from "$lib/types/scagnostics";
  import type { Scagnostic } from "$lib/types/scagnostics";
  import DoiConfig from "$lib/widgets/doi-config.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import Column from "$lib/widgets/column.svelte";
  import { sendScagnosticWeights } from "$lib/util/requests";

  export let maxWidth: number;

  let selectedWeights = new Map<Scagnostic, number>();

  const isSelected = {};
  scagnostics.forEach((s) => (isSelected[s] = false));
  $selectedScagnostics.forEach((s) => (isSelected[s] = true));

  $: $selectedScagnostics = scagnostics.filter((s) => isSelected[s]);
  $: selectedWeights.forEach((value, key) => $scagnosticWeights.set(key, value));

  selectedScagnostics.subscribe((newSelection) => {
    selectedWeights = new Map();
    newSelection.forEach((scagnostic) => {
      selectedWeights.set(scagnostic, $scagnosticWeights.get(scagnostic));
    });
  });

  function toggleAll() {
    if ($selectedScagnostics.length === scagnostics.length) {
      // deselect all
      scagnostics.forEach((s) => (isSelected[s] = false));
    } else {
      // select all
      scagnostics.forEach((s) => (isSelected[s] = true));
    }
  }
</script>

<DoiConfig
  title="Configure Scagnostics"
  message="Define the scatterplot diagnostics that interest you and set their weights."
  width={500}
>
  <Column>
    <div class="top-row">
      <h3 style="margin-top:0;">Select interesting scagnostics</h3>
      <button on:click={toggleAll}>
        {#if $selectedScagnostics.length === scagnostics.length}
          Deselect all
        {:else}
          Select all
        {/if}
      </button>
    </div>
    <div class="scagnostic-checklist" style="max-width:{maxWidth}px">
      {#each scagnostics as scagnostic}
        <div class="item">
          <input
            id={scagnostic}
            type="checkbox"
            value={scagnostic}
            bind:checked={isSelected[scagnostic]}
          />
          <label for={scagnostic}>{scagnostic}</label>
        </div>
      {/each}
    </div>
  </Column>

  <Column>
    <h3>Assign weights</h3>
    <WeightedValues
      group="selected-scagnostics"
      totalSize={maxWidth}
      bind:valueWeights={selectedWeights}
      on:end={() => sendScagnosticWeights($scagnosticWeights)}
    />
    {#if selectedWeights.size === 0}
      <p class="empty">Select interesting scagnostics above.</p>
    {/if}
  </Column>
</DoiConfig>

<style>
  div.top-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  div.top-row button {
    margin-bottom: 20px;
    background: white;
    border: 1px solid black;
    border-radius: 4px;
    padding: 4px 10px;
    color: black;
    cursor: pointer;
    transition: background 0.05s ease-in-out;
  }
  div.top-row button:hover {
    background: #efefef;
  }
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
  div.scagnostic-checklist div.item input:checked + label {
    background: black;
    color: white;
  }
  p.empty {
    margin: 0;
    color: #999;
  }
</style>
