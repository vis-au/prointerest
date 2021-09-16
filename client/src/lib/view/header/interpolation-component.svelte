<script lang="typescript">
  import { componentWeights } from "$lib/state/active-doi-weights";
  import { selectedDoiInterpolationFunction } from "$lib/state/selected-doi-interpolation-function";
  import { selectedDoiComponent } from "$lib/state/selected-doi-weight";
  import { functionNames } from "$lib/types/doi-interpolation-function";
  import { sendComponentWeights } from "$lib/util/requests";
  import Dropdown from "$lib/widgets/dropdown.svelte";
  import Row from "$lib/widgets/row.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";

  // let useProgression = true;
</script>

<Row id="component-weights" style="align-items:stretch">
  <h2>Configure DOI Components</h2>
  <WeightedValues
    group="doi-interpolation"
    totalSize={400}
    useDarkmode={true}
    bind:activeWeight={$selectedDoiComponent}
    bind:valueWeights={$componentWeights}
    on:end={() => sendComponentWeights($componentWeights)}
  />

  <Dropdown
    id="doi-interpolation-function"
    style="width:125px"
    useDarkMode={true}
    bind:selectedValue={$selectedDoiInterpolationFunction}
  >
    {#each functionNames as name}
      <option value={name} selected={name === $selectedDoiInterpolationFunction}>{name}</option>
    {/each}
  </Dropdown>

  <!-- <Toggle
    bind:active={useProgression}
    on:changed={() => {
      if (useProgression) {
        weights.set("prior", ($processedData.length / $totalSize));
        weights.set("posterior", 1 - ($processedData.length / $totalSize));
        weights = weights;
      }
    }}>bind to progression</Toggle> -->
</Row>

<style>
  :global(#doi-interpolation-function) {
    width: 100px;
    margin-left: 20px;
  }
  h2 {
    font-size: 12pt;
    margin: 0;
    margin-right: 20px;
    display: flex;
    align-items: center;
  }
</style>
