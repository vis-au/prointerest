<script lang="typescript">
  import { componentWeights } from "$lib/state/active-doi-weights";
import { selectedDoiInterpolationFunction } from "$lib/state/selected-doi-interpolation-function";
import { functionNames } from "$lib/types/doi-interpolation-function";
  import { getInterpolatedDoiValue } from "$lib/util/get-interpolated-doi-value";
  import Dropdown from "$lib/widgets/dropdown.svelte";
  import Row from "$lib/widgets/row.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";

  // let useProgression = true;

  $: console.log(selectedDoiInterpolationFunction, getInterpolatedDoiValue($componentWeights.get("prior")));
</script>

<Row id="component-weights" style="align-items:stretch">
  <WeightedValues
    group="doi-interpolation"
    totalSize={200}
    useDarkmode={true}
    bind:valueWeights={$componentWeights}
  />

  <Dropdown id="doi-interpolation-function" bind:selectedValue={$selectedDoiInterpolationFunction} style="margin-right: 10px">
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
</style>