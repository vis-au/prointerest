<script>

import { selectedOutlierMeasure } from "$lib/state/selected-outlier-measure";
import { outliernessMeasures } from "$lib/types/outlier-measures";
import Alternatives from "$lib/widgets/alternatives.svelte";
import DoiConfig from "$lib/widgets/doi-config.svelte";

</script>


<DoiConfig
  title="Set outlier measure"
  message="You can choose between three different outlierness metrics that are used to determine whether a data item is an outlier or not."
  width={ 400 }>

  <Alternatives
    name="outlierness-measure"
    alternatives={ outliernessMeasures }
    bind:activeAlternative={ $selectedOutlierMeasure }
  />

</DoiConfig>
