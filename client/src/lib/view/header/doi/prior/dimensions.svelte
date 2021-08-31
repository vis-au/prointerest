<script lang="typescript">

import { dimensions } from "$lib/state/processed-data";
import { selectedDimensionsOfInterest } from "$lib/state/selected-dimensions-of-interest";
import DoiConfig from "$lib/widgets/doi-config.svelte";

</script>


<DoiConfig title="Select Dimension of Interest">
  { #each $dimensions as dim }
    <div class="row">
      <label for={ dim }>{ dim }</label>
      <input type="checkbox" value={ dim } checked={ $selectedDimensionsOfInterest.indexOf(dim) > -1 } id={ dim } on:change={ () => {
        const index = $selectedDimensionsOfInterest.indexOf(dim);
        if (index > -1) {
          $selectedDimensionsOfInterest.splice(index, 1);
        } else {
          $selectedDimensionsOfInterest.push(dim);
        }
      }} />
    </div>
  { /each }
</DoiConfig>