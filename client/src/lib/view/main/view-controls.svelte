<script>
  import { scatterplotBrush } from "$lib/state/active-scatterplot-brush";
  import { activeViewEncodings } from "$lib/state/active-view-encodings";
  import { activeViewMode } from "$lib/state/active-view-mode";
  import { doiLimit } from "$lib/state/doi-limit";
  import { doiValues } from "$lib/state/doi-values";
  import { isRecentChunkVisible } from "$lib/state/is-recent-chunk-visible";
  import { dimensions } from "$lib/state/processed-data";
  import { resetViewTransform } from "$lib/state/zoom";
  import { brushModes } from "$lib/types/brush-mode";
  import { colorEncodings, sizeEncodings } from "$lib/types/encodings";
  import { viewModes } from "$lib/types/view-modes";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import ControlButton from "$lib/widgets/control-button.svelte";
  import Dropdown from "$lib/widgets/dropdown.svelte";
  import HistogramSlider from "$lib/widgets/histogram-slider.svelte";
  import Row from "$lib/widgets/row.svelte";
  import Toggle from "$lib/widgets/toggle.svelte";
  import { bin } from "d3";

  let binsGenerator = bin().thresholds(25);
  $: doiBins = binsGenerator(Array.from($doiValues.values()).concat(0, 1)).map((d) => d.length);
</script>

<Row id="view-controls">
  <div class="configuration">
    <h2>View</h2>
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
      <h2>Color</h2>
      <Alternatives
        name="hexbin-color-encoding"
        alternatives={colorEncodings}
        bind:activeAlternative={$activeViewEncodings.color}
      />
    {/if}
    <ControlButton on:click={resetViewTransform} style="margin-left:25px;padding:2px 10px">
      reset zoom
    </ControlButton>
  </div>
  <div class="configuration">
    <Toggle id="show-recent-chunk" bind:active={$isRecentChunkVisible}>Show recent chunk</Toggle>
  </div>
  <div class="configuration">
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
  </div>
  <div class="configuration">
    <h2>Brush</h2>
    <Alternatives
      name="scatterplot-brush-mode"
      alternatives={brushModes}
      bind:activeAlternative={$scatterplotBrush}
    />
  </div>
  <div class="configuration">
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
  </div>
</Row>

<style>
  :global(div#view-controls) {
    position: absolute;
    top: 0;
    box-sizing: border-box;
    justify-content: space-around;
    width: 100%;
    background: rgba(255, 255, 255, 0.73);
    padding: 5px 30px;
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

  div.configuration {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-right: 10px;
  }

  h2 {
    font-weight: normal;
    margin: 0 5px;
    padding: 0;
  }
</style>
