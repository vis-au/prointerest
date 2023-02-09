<script lang="ts">
  import { Deck, OrthographicView } from "@deck.gl/core";
  import { ScatterplotLayer } from "@deck.gl/layers";
  import { rgb } from "d3";
  import { selectAll } from "d3-selection";
  import { afterUpdate, onMount } from "svelte";

  import { colorScale } from "$lib/state/active-color-scale";
  import { activeViewEncodings, rgbToColorArray } from "$lib/state/active-view-encodings";
  import { doiValues } from "$lib/state/doi-values";
  import { interestingItems } from "$lib/state/items";
  import { randomDataSample } from "$lib/state/sampled-data";
  import { currentTransform, isZooming } from "$lib/state/zoom";
  import type DataItem from "$lib/types/data-item";

  export let id = "deck-gl-scatterplot";
  export let width = 100;
  export let height = 50;
  export let radius = 2; // size of points
  export let orientation = "right"; // left or right side of the screen?

  $: interestingData = $isZooming ? $randomDataSample : $interestingItems;

  const INITIAL_VIEW_STATE = {
    zoom: 0,
    minZoom: -1,
    maxZoom: 40,
    orthographic: true
  };

  let canvasElement: HTMLCanvasElement;

  $: layers = [];
  $: views = [];

  onMount(() => {
    window.setInterval(() => {
      selectAll("div.deck-tooltip").remove();
    }, 1000);
  });

  afterUpdate(render);

  function render() {
    INITIAL_VIEW_STATE["target"] = [width / 2, height / 2, 0];

    const t = $currentTransform;

    const color = $colorScale.copy();
    color.domain([0, 1]);

    const getFillColor = $activeViewEncodings.color === "doi"
      ? (d: DataItem) => rgbToColorArray(rgb(color($doiValues.get(d.id))))
      : [0, 0, 0];

    layers = [
      new ScatterplotLayer({
        id: `${id}-layer`,
        opacity: 0.1,
        getPosition: (d: DataItem) => [t.applyX(d.position.x), t.applyY(d.position.y)],
        getRadius: radius,
        getLineWidth: 0,
        getFillColor,
        lineWidthUnits: "pixels",
        stroked: false,
        data: interestingData
      })
    ];

    views = [
      new OrthographicView({
        id: `${id}-view`,
        flipY: true,
        controller: false,
        x: 0,
        y: 0,
        width: width,
        height: height
      })
    ];

    generateDeckComponent();
  }

  function generateDeckComponent() {
    const style =
      orientation === "left"
        ? { left: "0", border: "none", position: "" }
        : { right: "0", border: "none", position: "" };

    style.position = "relative";

    new Deck({
      id: id,
      canvas: canvasElement,
      width,
      height,
      views,
      layers,
      style,
      initialViewState: INITIAL_VIEW_STATE
    });
  }
</script>

<div id="{id}-scatterplot-view" class="scatterplot-view">
  <canvas
    id="{id}-scatterplot-view-canvas"
    class="scatterplot-view"
    {width}
    {height}
    bind:this={canvasElement}
  />
</div>

<style>
  div.scatterplot-view {
    position: relative;
  }
  div.scatterplot-view canvas.scatterplot-view {
    position: absolute;
  }
</style>
