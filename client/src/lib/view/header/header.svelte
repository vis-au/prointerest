<script lang="ts">
  import ProgressionControls from "../main/progression-controls.svelte";
  import { scagnosticWeights, selectedScagnostics } from "$lib/state/selected-scagnostics";
  import { scagnostics } from "$lib/types/scagnostics";
  import { sendScagnosticWeights } from "$lib/util/requests";
  import type { Scagnostic } from "$lib/types/scagnostics";
  import Row from "$lib/widgets/row.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import Options from "$lib/widgets/options.svelte";

  export let height: number;

  const maxWidth = 700;
  let selectedWeights = new Map<Scagnostic, number>();

  let isSelected = {};
  scagnostics.forEach((s) => (isSelected[s] = false));
  $selectedScagnostics.forEach((s) => (isSelected[s] = true));

  $: selectedWeights.forEach((value, key) => $scagnosticWeights.set(key, value));
  $: $selectedScagnostics = scagnostics.filter((s) => isSelected[s]);

  selectedScagnostics.subscribe((newSelection) => {
    selectedWeights = new Map();
    newSelection.forEach((scagnostic) => {
      selectedWeights.set(scagnostic, $scagnosticWeights.get(scagnostic));
    });
  });

  function removeScagnostic(event: CustomEvent<string>) {
    isSelected[event.detail] = false;
  }
</script>

<header style="height:{height}px">
  <div class="title">
    <img src="static/logo.svg" alt="the ProInterest logo" height={height * 0.8} />
  </div>
  <Row>
    <Row id="doi-configuration" style="align-items:center;height:{height * 0.8}px;flex-grow: 5">
      <h2>Configure DOI:</h2>
      <WeightedValues
        id="selected-scagnostics"
        totalSize={maxWidth}
        weightsRemovable={true}
        useDarkmode={true}
        backgroundColor="#008080"
        isSelectable={false}
        bind:valueWeights={selectedWeights}
        on:remove-weight={removeScagnostic}
        on:end={() => sendScagnosticWeights($scagnosticWeights)}
      />
      <Options
        options={scagnostics}
        showActive={false}
        showInactive={false}
        bind:activeOptions={isSelected}
        useDarkMode={true}
        style="margin-left: 25px"
      />
    </Row>
  </Row>
  <ProgressionControls useAbsolutePositioning={false} useDarkMode={true} style="flex-grow:0" />
</header>

<style>
  header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    background: #333;
    color: #fff;
    border-bottom: 1px solid #ddd;
  }

  h2 {
    margin: 0;
    margin-right: 25px;
    padding: 0;
    font-size: 18px;
    font-weight: bold;;
  }

  header div.title {
    margin-left: 2px;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
</style>
