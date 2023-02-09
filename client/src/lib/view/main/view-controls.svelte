<script>
  import { bin } from "d3";

  import { scatterplotBrush } from "$lib/state/active-scatterplot-brush";
  import { activeViewEncodings } from "$lib/state/active-view-encodings";
  import { activeViewMode } from "$lib/state/active-view-mode";
  import { doiLimit } from "$lib/state/doi-limit";
  import { averageDoiPerChunk, doiValues } from "$lib/state/doi-values";
  import { hexbinRadius } from "$lib/state/hexbinning";
  import { isRecentChunkVisible, isOnlyInterestingRecentDataVisible } from "$lib/state/is-recent-chunk-visible";
  import { dimensions } from "$lib/state/processed-data";
  import { resetViewTransform } from "$lib/state/zoom";
  import { brushModes } from "$lib/types/brush-mode";
  import { colorEncodings, sizeEncodings } from "$lib/types/encodings";
  import { viewModes } from "$lib/types/view-modes";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import ControlButton from "$lib/widgets/control-button.svelte";
  import Dropdown from "$lib/widgets/dropdown.svelte";
  import HistogramSlider from "$lib/widgets/histogram-slider.svelte";
  import MiniHistogram from "$lib/widgets/mini-histogram.svelte";
  import Row from "$lib/widgets/row.svelte";
  import Slider from "$lib/widgets/slider.svelte";
  import Toggle from "$lib/widgets/toggle.svelte";
  import ViewConfigurationPanel from "./view-configuration-panel.svelte";

  let binsGenerator = bin().thresholds(25);
  $: doiBins = binsGenerator(Array.from($doiValues.values()).concat(0, 1)).map((d) => d.length);
</script>

<Row id="view-controls">
  <ViewConfigurationPanel label="DOI" active={true}>
    <HistogramSlider
      id="doi-limit"
      label="DOI limit"
      width={300}
      min={0}
      max={1}
      updateLive={false}
      values={doiBins}
      bind:value={$doiLimit}
    />
    <h2>avg doi/chunk:</h2>
    <MiniHistogram
      id="mean-doi-per-chunk"
      domain={[0, 1]}
      width={100}
      height={25}
      values={$averageDoiPerChunk}
      histogramStyle="padding:0 5px;"
    />
    <!-- <h2>doi ages</h2>
    <MiniHistogram
      id="doi-age-per-item"
      domain={[0, max($doiAgeHistogram.map((d) => d.length))]}
      width={100}
      height={25}
      values={$doiAgeHistogram.map((d) => d.length)}
      histogramStyle="padding:0 5px;"
    /> -->
  </ViewConfigurationPanel>

  <ViewConfigurationPanel label="View">
    <Alternatives
      name="view-modes"
      alternatives={viewModes}
      bind:activeAlternative={$activeViewMode}
    />
    {#if $activeViewMode === "binned"}
      <h2>Size</h2>
      <Alternatives
        name="hexbin-size-encoding"
        alternatives={sizeEncodings}
        bind:activeAlternative={$activeViewEncodings.size}
      />
      <Slider
        id="hexbin-radius"
        label="r"
        width={100}
        sliderWidth={80}
        min={1}
        max={50}
        bind:value={$hexbinRadius}
        showValue={false}
        updateLive={true}
        showDomain={false}
      />
    {/if}
    <h2>Color</h2>
    <Alternatives
      name="hexbin-color-encoding"
      alternatives={colorEncodings}
      bind:activeAlternative={$activeViewEncodings.color}
    />
    <ControlButton on:click={resetViewTransform} style="margin-left:25px;padding:2px 10px">
      reset zoom
    </ControlButton>
  </ViewConfigurationPanel>

  <ViewConfigurationPanel label="Chunk">
    <Toggle id="show-recent-chunk" bind:active={$isRecentChunkVisible}>Highlight recent</Toggle>
    {#if $isRecentChunkVisible}
      <Toggle id="show-only-interesting-recent-chunk"  bind:active={$isOnlyInterestingRecentDataVisible}>Only interesting</Toggle>
    {/if}
  </ViewConfigurationPanel>

  <ViewConfigurationPanel label="Axes">
    <h2>Axes</h2>
    <Dropdown id="x-encoding" className="encoding" bind:selectedValue={$activeViewEncodings.x}>
      {#each $dimensions as dim}
        <option>{dim}</option>
      {/each}
    </Dropdown>
    <Dropdown id="y-encoding" className="encoding" bind:selectedValue={$activeViewEncodings.y}>
      {#each $dimensions as dim}
        <option>{dim}</option>
      {/each}
    </Dropdown>
  </ViewConfigurationPanel>

  <ViewConfigurationPanel label="Brush">
    <Alternatives
      name="scatterplot-brush-mode"
      alternatives={brushModes}
      bind:activeAlternative={$scatterplotBrush}
    />
  </ViewConfigurationPanel>
</Row>

<style>
  :global(div#view-controls) {
    position: absolute;
    top: 0;
    box-sizing: border-box;
    justify-content: flex-start;
    align-items: stretch;
    width: 100%;
    background: rgba(255, 255, 255, 0.73);
    padding: 5px;
    border-radius: 4px;
  }

  :global(#view-controls *) {
    font-size: 12pt;
  }

  :global(.show-me) {
    margin-left: 10px;
  }

  :global(div.configuration .encoding) {
    max-width: 150px;
    margin: 0 5px;
  }

  h2 {
    font-weight: normal;
    margin: 0 5px;
    padding: 0;
  }
</style>
