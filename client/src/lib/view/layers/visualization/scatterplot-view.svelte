<script lang="ts">
  import { afterUpdate, onMount } from "svelte";
  import { Deck, OrthographicView } from "@deck.gl/core";
  import { ScatterplotLayer } from "@deck.gl/layers";
  import { selectAll } from "d3-selection";

  import { currentTransform } from "$lib/state/zoom";
  import type DataItem from "$lib/types/data-item";
  import { visibleInterestingData } from "$lib/state/visible-data";

  export let id = "deck-gl-scatterplot";
  export let width = 100;
  export let height = 50;
  export let radius = 5; // size of points
  export let orientation = "right"; // left or right side of the screen?

  $: data = $visibleInterestingData;

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

    layers = [
      new ScatterplotLayer({
        id: `${id}-layer`,
        getPosition: (d: DataItem) => [t.applyX(d.position.x), t.applyY(d.position.y)],
        getRadius: radius,
        getLineWidth: 0,
        opacity: 0.01,
        lineWidthUnits: "pixels",
        stroked: false,
        data: data
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
