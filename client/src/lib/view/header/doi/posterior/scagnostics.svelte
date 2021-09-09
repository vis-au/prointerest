<script lang="typescript">
  import { scagnosticWeights, selectedScagnostics } from "$lib/state/selected-scagnostics";
  import { scagnostics } from "$lib/types/scagnostics";
  import type { Scagnostic } from "$lib/types/scagnostics";
  import DoiConfig from "$lib/view/header/doi/doi-config.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import Column from "$lib/widgets/column.svelte";
  import { sendScagnosticWeights } from "$lib/util/requests";
  import Options from "$lib/widgets/options.svelte";

  const maxWidth = 700;
  let selectedWeights = new Map<Scagnostic, number>();

  let isSelected = {};
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
    <Options
      options={scagnostics}
      bind:activeOptions={isSelected}
    />
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
  p.empty {
    margin: 0;
    color: #999;
  }
</style>
