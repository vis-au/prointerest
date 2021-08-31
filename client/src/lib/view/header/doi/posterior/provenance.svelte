<script>
import { interactionWeights } from "$lib/state/interaction-technique-weights";

import Column from "$lib/widgets/column.svelte";
import DoiConfig from "$lib/widgets/doi-config.svelte";
import WeightedValues from "$lib/widgets/weighted-values.svelte";

</script>


<DoiConfig title="Configure Provenance">
  <Column>
    <h3>Assign weights to interactions</h3>
    <WeightedValues
      group="interaction-technique-weights"
      valueWeights={ $interactionWeights }
      totalSize={ 400 }
    />
  </Column>
</DoiConfig>