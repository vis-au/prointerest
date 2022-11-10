<script>
  import { scatterplotBrush } from "$lib/state/active-scatterplot-brush";
  import { activeBinMode } from "$lib/state/active-bin-mode";
  import { activeViewEncodings } from "$lib/state/active-view-encodings";
  import { activeViewMode } from "$lib/state/active-view-mode";
  import { isRecentChunkVisible } from "$lib/state/is-recent-chunk-visible";
  import { dimensions } from "$lib/state/processed-data";
  import { binModes } from "$lib/types/bin-mode";
  import { brushModes } from "$lib/types/brush-mode";
  import { viewModes } from "$lib/types/view-modes";
  import Alternatives from "$lib/widgets/alternatives.svelte";
  import Dropdown from "$lib/widgets/dropdown.svelte";
  import Row from "$lib/widgets/row.svelte";
  import Slider from "$lib/widgets/slider.svelte";
  import { doiLimit } from "$lib/state/doi-limit";
  import Toggle from "$lib/widgets/toggle.svelte";
</script>

<Row id="view-controls">
  <div class="configuration">
    <h2>View</h2>
    <Alternatives
      name="view-modes"
      alternatives={viewModes}
      bind:activeAlternative={$activeViewMode}
    />
  </div>
  <div class="configuration">
    <h2>Recent</h2>
    <Toggle
      id="show-recent-chunk"
      bind:active={$isRecentChunkVisible}
    />
  </div>
  <div class="configuration">
    <h2>Bin by</h2>
    <Alternatives
      name="bin-modes"
      alternatives={binModes}
      bind:activeAlternative={$activeBinMode}
    />
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
    <Slider
      id="doi-limit"
      label="DOI limit"
      width={300}
      min={0}
      max={1}
      bind:value={$doiLimit}
    />
  </div>
</Row>

<style>
  :global(div#view-controls) {
    position: absolute;
    box-sizing: border-box;
    justify-content: space-around;
    padding-top: 20px;
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
