<script lang="typescript">
import { selectedDimensionsOfInterest } from "$lib/state/selected-dimensions-of-interest";
import { selectedItems } from "$lib/state/selected-items";
import { arrayItemToRecord } from "$lib/util/item-transform";

import DoiConfig from "$lib/widgets/doi-config.svelte";
import Histogram from "$lib/widgets/histogram.svelte";


$: tabularData = $selectedItems.map(arrayItemToRecord);
</script>

<DoiConfig
  title="Selected Data Items"
  width={ 400 }
  message="Visualizes the distributions in the data items selected as interesting using the brush across all dimensions marked as interesting."
>
  { #each $selectedDimensionsOfInterest as dim, i }
    <div class="dimension">
      <h3>{dim}</h3>
      <Histogram
        id="doi-selected-dim-{i}"
        data={ tabularData }
        dimension={ i+"" }
        width={ 300 }
        height={ 50 }
      />
    </div>
  { /each }
</DoiConfig>

<style>
  h3 {
    margin: 0;
    font-size: 10pt;
  }
</style>