<script lang="typescript">
  import { currentTransform, isZooming } from "$lib/state/zoom";

  import { zoom, zoomTransform } from "d3-zoom";
  import type { D3ZoomEvent } from "d3-zoom";
  import { select } from "d3-selection";
  import type { Selection } from "d3-selection";
  import { afterUpdate, createEventDispatcher, onMount } from "svelte";

  export let id: string;
  export let className: string;
  export let width: number;
  export let height: number;

  let zoomCanvasElement: HTMLCanvasElement;

  const dispatch = createEventDispatcher();

  const zoomBehavior = zoom()
    .scaleExtent([0.75, 10])
    .on("start", () => ($isZooming = true))
    .on("zoom", onZoom)
    .on("end", onZoomEnd);

  function onZoom(event: D3ZoomEvent<Element, void>) {
    if (event.sourceEvent === null) {
      return;
    }

    $currentTransform = event.transform;
  }

  function onZoomEnd() {
    $isZooming = false;

    // const interaction = interactionFactory.createZoomInteraction($currentTransform);
    // onInteraction(interaction);
    dispatch("end", $currentTransform);
  }

  onMount(() => {
    const zoomCanvas = select(zoomCanvasElement);
    zoomCanvas.call(zoomBehavior);
  });

  afterUpdate(() => {
    const canvas = select(zoomCanvasElement) as Selection<Element, unknown, null, null>;
    const myZoom = zoomTransform(zoomCanvasElement);

    // check if the zoom transform has changed
    if (JSON.stringify(myZoom) !== JSON.stringify($currentTransform)) {
      zoomBehavior.transform(canvas, $currentTransform);
    }
  });
</script>

<canvas
  id="{id}-zoom-canvas"
  class="zoom interaction-canvas {className}"
  {width}
  {height}
  on:mousemove={(e) => dispatch("hover", e)}
  on:click={(e) => dispatch("click", e)}
  bind:this={zoomCanvasElement}
/>

<style>
  canvas.interaction-canvas.hidden {
    display: none;
  }
</style>
