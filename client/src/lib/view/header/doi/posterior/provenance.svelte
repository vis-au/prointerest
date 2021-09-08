<script>
  import { interactionWeights } from "$lib/state/interaction-technique-weights";
  import Column from "$lib/widgets/column.svelte";
  import DoiConfig from "$lib/widgets/doi-config.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";

  // TODO: widget to define, how long the interaction log should be
  // TODO: suggest similar/dissimlar data based on prior/posterior/both
</script>

<DoiConfig
  title="Configure Provenance"
  message="Configure how much weight each interaction should be assigned to, when computing the data of interest."
  width={400}
>
  <Column>
    <h3>Assign weights to interactions</h3>
    <WeightedValues
      group="interaction-technique-weights"
      totalSize={310}
      bind:valueWeights={$interactionWeights}
    />
  </Column>
</DoiConfig>
