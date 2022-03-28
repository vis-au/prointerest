<script lang="ts">
  import { priorWeights } from "$lib/state/active-doi-weights";
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
  import { sendWeights } from "$lib/util/requests";
  import Row from "$lib/widgets/row.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
</script>

<Row style="align-items:stretch">
  <h2>Prior</h2>
  <WeightedValues
    id="doi-weights"
    totalSize={400}
    backgroundColor="#80b1d3"
    useDarkmode={true}
    bind:valueWeights={$priorWeights}
    bind:activeWeight={$selectedDoiWeight}
    on:end={() => sendWeights("prior", $priorWeights)}
  />
</Row>

<style>
  h2 {
    display: flex;
    align-items: center;
    margin: 0;
    font-size: 12pt;
    margin-right: 10px;
    margin-left: 30px;
  }
</style>
