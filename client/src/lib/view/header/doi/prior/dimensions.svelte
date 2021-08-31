<script lang="typescript">

import { dimensions, processedData } from "$lib/state/processed-data";
import { selectedDimensionsOfInterest } from "$lib/state/selected-dimensions-of-interest";
import { arrayItemToRecord } from "$lib/util/item-transform";
import DoiConfig from "$lib/widgets/doi-config.svelte";
import Histogram from "$lib/widgets/histogram.svelte";
import Row from "$lib/widgets/row.svelte";

$: tabularData = $processedData.map(arrayItemToRecord);

const isInteresting = {};
$dimensions.forEach(dim => isInteresting[dim] = false);
$selectedDimensionsOfInterest.forEach(dim => isInteresting[dim] = true);

$: $selectedDimensionsOfInterest = $dimensions.filter(dim => isInteresting[dim]);

</script>


<DoiConfig
  width={ 400 }
  title="Select Dimension of Interest"
  message="Visualizes overall distributions in the dataset, allows defining regions of interest.">
  { #each $dimensions as dim, i }
    <Row>
      <label for={ dim }>{ dim }</label>
      <input id={ dim } type=checkbox value={ dim } bind:checked={ isInteresting[dim] } />

      { #if $selectedDimensionsOfInterest.indexOf(dim) > -1 }
        <Histogram
          id="all-data-dim-{i}"
          data={ tabularData }
          dimension={ i+"" }
          width={ 300 }
          height={ 50 }
        />
      { /if }
    </Row>
  { /each }
</DoiConfig>