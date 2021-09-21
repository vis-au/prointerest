<script lang="typescript">
  import { outliernessWeights } from "$lib/state/active-doi-weights";
  import { selectedOutlierMeasure } from "$lib/state/selected-outlier-measure";
  import { sendWeights } from "$lib/util/requests";
  import DoiConfig from "$lib/view/header/doi/doi-panel.svelte";
  import WeightedValues from "$lib/widgets/weighted-values.svelte";
  import BigNumber from "$lib/widgets/big-number.svelte";

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
    {#if $selectedOutlierMeasure === "tukey"}
      The "tukey" measure captures outlierness by determining, if the item falls outside the Tukey
      ranges across <BigNumber>75%</BigNumber> of the data.
    {:else if $selectedOutlierMeasure === "scagnostic"}
      The "scagnostics" measure captures outlierness by determining if the item returns an
      outlierness scagnostic value of greater than <BigNumber>.95</BigNumber>.
    {:else if $selectedOutlierMeasure === "clustering"}
      The "clustering" measure captures outlierness by determining, if the item is assigned its own
      cluster when applying DBSCAN to the data.
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
