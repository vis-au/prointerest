<script lang="typescript">
  import type { D3BrushEvent } from "d3-brush";
  import { brush } from "d3-brush";
  import { geoPath } from "d3-geo";
  import type { GeoPermissibleObjects } from "d3-geo";
  import { select } from "d3-selection";

  import { createEventDispatcher, onMount } from "svelte";

  import { activeBrush, activeLasso } from "$lib/state/active-brush";
  import { scatterplotBrush } from "$lib/state/active-scatterplot-brush";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { currentTransform } from "$lib/state/zoom";
  import type DataItem from "$lib/types/data-item";
  import { lasso } from "$lib/util/lasso-brush";

  export let id: string;
  export let className: string;
  export let width: number;
  export let height: number;

  let brushCanvasElement: SVGElement;
  let lassoCanvasElement: SVGElement;

  const dispatch = createEventDispatcher();

  const brushBehavior = brush()
    .keyModifiers(false)
    .filter((event) => (event.ctrlKey || event.shiftKey) && !event.button)
    .on("end", onBrushEnd);

  const lassoBehavior = lasso().on("start lasso", onLassoBrush).on("end", onLassoEnd);

  function onBrushEnd(event: D3BrushEvent<DataItem>) {
    const selection = event.selection;

    if (selection === null || selection === undefined) {
      $activeBrush = null;
      return;
    }

    const [[x0, y0], [x1, y1]] = selection as [[number, number], [number, number]];
    const _x0 = $scaleX.invert($currentTransform.invertX(x0));
    const _y0 = $scaleY.invert($currentTransform.invertY(y0));
    const _x1 = $scaleX.invert($currentTransform.invertX(x1));
    const _y1 = $scaleY.invert($currentTransform.invertY(y1));
    $activeBrush = [
      [_x0, _y0],
      [_x1, _y1]
    ];

    // the brush is drawn by the brush-layer component to make the brushed region persist zoom+pan
    // we can therefore hide it here
    select(brushCanvasElement).selectAll("rect.selection,rect.handle").style("display", "none");

    dispatch("end", $activeBrush);
  }

  function onLassoBrush(polygon: [number, number][]) {
    const svg = select(lassoCanvasElement);
    const path = geoPath();

    svg.select("path.lasso").remove();

    const l = svg.append("path").attr("class", "lasso");

    l.datum({ type: "LineString", coordinates: polygon })
      .attr("fill", "rgba(0, 0, 0, 0.05)")
      .attr("stroke", "#333")
      .attr("stroke-width", 2)
      .attr("d", (d) => path(d as GeoPermissibleObjects));
  }

  function onLassoEnd(polygon: [number, number][]) {
    if (!polygon.length) {
      $activeLasso = null;
      return;
    }

    const t = $currentTransform;
    $activeLasso = polygon.map((p) => [
      $scaleX.invert(t.invertX(p[0])),
      $scaleY.invert(t.invertY(p[1]))
    ]);

    // lasso is drawn by brush-layer component, so remove it here.
    select(lassoCanvasElement).select("path.lasso").remove();

    dispatch("end", $activeLasso);
  }

  onMount(() => {
    // use a timeout to ensure that the brush canvas has the right size when calling the brush
    // behavior
    setTimeout(() => {
      select(brushCanvasElement).call(brushBehavior);
      select(lassoCanvasElement).call(lassoBehavior);
    }, 10);
  });
</script>

<div class="{className} interaction-canvas container" style="width:{width}px;height:{height}px">
  <svg
    id="{id}-brush-canvas"
    class="brush {className} {$scatterplotBrush === 'rect' ? '' : 'hidden'}"
    {width}
    {height}
    bind:this={brushCanvasElement}
    on:mousemove={(e) => dispatch("hover", e)}
    on:click={(e) => dispatch("click", e)}
  />
  <svg
    id="{id}-lasso-canvas"
    class="lasso {className} {$scatterplotBrush === 'lasso' ? '' : 'hidden'}"
    {width}
    {height}
    bind:this={lassoCanvasElement}
    on:mousemove={(e) => dispatch("hover", e)}
    on:click={(e) => dispatch("click", e)}
  />
</div>

<style>
  div.container {
    position: absolute;
  }
  svg {
    cursor: crosshair;
    position: absolute;
  }
  svg.hidden {
    display: none;
  }
</style>
