<script lang="typescript">

import { dimensions, processedData } from "$lib/state/processed-data";
import { selectedDimensionsOfInterest } from "$lib/state/selected-dimensions-of-interest";
import { arrayItemToRecord } from "$lib/util/item-transform";
import DoiConfig from "$lib/widgets/doi-config.svelte";
import Histogram from "$lib/widgets/histogram.svelte";
import Row from "$lib/widgets/row.svelte";

$: tabularData = $processedData.map(arrayItemToRecord);

</script>


<DoiConfig
  width={ 400 }
  title="Select Dimension of Interest"
  message="Visualizes overall distributions in the dataset, allows defining regions of interest.">
  { #each $dimensions as dim, i }
    <Row>
      <label for={ dim }>{ dim }</label>
      <input type="checkbox" value={ dim } checked={ $selectedDimensionsOfInterest.indexOf(dim) > -1 } id={ dim } on:change={ () => {
        const index = $selectedDimensionsOfInterest.indexOf(dim);
        if (index > -1) {
          $selectedDimensionsOfInterest.splice(index, 1);
        } else {
          $selectedDimensionsOfInterest.push(dim);
        }
      }} />

      <div class="dimension">
        <Histogram
          id="all-data-dim-{i}"
          data={ tabularData }
          dimension={ i+"" }
          width={ 300 }
          height={ 50 }
        />
      </div>
    </Row>
  { /each }
</DoiConfig>