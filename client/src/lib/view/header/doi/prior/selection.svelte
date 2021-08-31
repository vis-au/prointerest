<script lang="typescript">
import { selectedDimensionsOfInterest } from "$lib/state/selected-dimensions-of-interest";
import { selectedItems } from "$lib/state/selected-items";
import { arrayItemToRecord } from "$lib/util/item-transform";
import BigNumber from "$lib/widgets/big-number.svelte";

import DoiConfig from "$lib/widgets/doi-config.svelte";
import Histogram from "$lib/widgets/histogram.svelte";


$: tabularData = $selectedItems.map(arrayItemToRecord);
</script>

<DoiConfig
  title="Inspect Selected Data Items"
  width={ 400 }
  message="Visualizes the distributions in the data items selected as interesting using the brush across all dimensions marked as interesting."
>
  <p class="selected">
    <BigNumber>{ $selectedItems.length }</BigNumber> items in selections.
  </p>
  <div class="histograms">
    { #each $selectedDimensionsOfInterest as dim, i }
      <div class="dimension">
        <h3>{dim}</h3>
        <Histogram
          id="doi-selected-dim-{i}"
          data={ tabularData }
          dimension={ i+"" }
          width={ 350 }
          height={ 50 }
        />
      </div>
    { /each }
  </div>
  { #if $selectedDimensionsOfInterest.length === 0 }
    <p class="message">Hint: No dimensions of interest specified. Use the "dimensions" component to do so.</p>
  { :else if $selectedItems.length === 0 }
    <p class="message">Hint: No items selected. You can use the brush or select individual bins.</p>
  { /if }
</DoiConfig>

<style>
  p.selected {
    margin-bottom: 20px;
  }
  span.count {
    font-weight: bold;
  }
  h3 {
    margin: 0;
    font-size: 10pt;
  }
  p.message {
    color: #999;
  }
</style>