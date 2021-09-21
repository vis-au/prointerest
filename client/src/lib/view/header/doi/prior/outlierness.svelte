<script lang="typescript">
  import { outliernessWeights } from "$lib/state/active-doi-weights";
  import { selectedOutlierMeasure } from "$lib/state/selected-outlier-measure";
  import { sendWeights } from "$lib/util/requests";
  import DoiConfig from "$lib/view/header/doi/doi-panel.svelte";
  import Link from "$lib/widgets/link.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";

  const width = 800;
</script>

<DoiConfig
  title="Configure outlier weights"
  message="You can choose between three different outlierness metrics that are used to determine whether a data item is an outlier or not."
  {width}
>
  <WeightedValues
    id="outlierness-weights"
    totalSize={width}
    height={40}
    bind:valueWeights={$outliernessWeights}
    bind:activeWeight={$selectedOutlierMeasure}
    on:end={() => sendWeights("outlierness", $outliernessWeights)}
  />
  <p class="explanation" style="max-width:{width}px">
    Info:
    {#if $selectedOutlierMeasure === "elliptic"}
      Apply sklearn's EllipticEnvelope metric.
      Check the <Link href="https://scikit-learn.org/stable/modules/generated/sklearn.covariance.EllipticEnvelope.html">documentation</Link> for more details.
    {:else if $selectedOutlierMeasure === "oneclass"}
      Apply sklearn's OneClassSVM metric.
      Check the <Link href="https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html">documentation</Link> for more details.
    {:else if $selectedOutlierMeasure === "forest"}
      Apply sklearn's IsolationForest metric.
      Check the <Link href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html">documentation</Link> for more details.
    {:else}
      Click on a measure above to learn more.
    {/if}
  </p>
</DoiConfig>

<style>
  p.explanation {
    color: #999;
  }
</style>
