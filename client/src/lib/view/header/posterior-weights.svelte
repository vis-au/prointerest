<script lang="typescript">

import { posteriorWeights } from "$lib/state/active-doi-weights";
import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
import Row from "$lib/widgets/row.svelte";
import WeightedValues from "$lib/widgets/weighted-values.svelte";

</script>

<Row>
  <h2>Posterior</h2>
  <WeightedValues
    group="doi-weights"
    valueWeights={ $posteriorWeights }
    totalSize={ 250 }
    bind:activeWeight={ $selectedDoiWeight }
  />
</Row>

<style>
  h2 {
    margin: 0;
    font-size: 12pt;
    margin-right: 10px;
    margin-left: 30px;
  }
</style>

