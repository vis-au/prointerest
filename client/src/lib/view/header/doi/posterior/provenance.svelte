<script>
import { interactionWeights } from "$lib/state/interaction-technique-weights";
import { dimensions } from "$lib/state/processed-data";
import { suggestedItems } from "$lib/state/suggested-items";
import { dataItemToRecord } from "$lib/util/item-transform";

import Column from "$lib/widgets/column.svelte";
import DoiConfig from "$lib/widgets/doi-config.svelte";
import Histogram from "$lib/widgets/histogram.svelte";
import WeightedValues from "$lib/widgets/weighted-values.svelte";

$: tabularData = $suggestedItems.map(dataItemToRecord);
</script>


<DoiConfig title="Configure Provenance" message="Configure how much weight each interaction should be assigned to, when computing the data of interest." width={ 400 }>
  <Column>
    <h3>Assign weights to interactions</h3>
    <WeightedValues
      group="interaction-technique-weights"
      valueWeights={ $interactionWeights }
      totalSize={ 310 }
    />
  </Column>
  <Column>
    <div class="histograms">
      { #each $dimensions as dim, i }
        <div class="dimension">
          <h3>{dim}</h3>
          <Histogram
            id="doi-selected-dim-{i}"
            data={ tabularData }
            dimension={ i+"" }
            width={ 310 }
            height={ 50 }
          />
        </div>
    { /each }
  </div>
  </Column>
</DoiConfig>


<style>
  div.histograms {
    margin-top: 30px;
  }
  div.dimension h3 {
    font-size: 10pt;
    margin: 0;
  }
</style>