<script lang="typescript">
  import type { D3BrushEvent } from "d3-brush";
  import { brush } from "d3-brush";
  import { select } from "d3-selection";

  import { createEventDispatcher, onMount } from "svelte";

  import { activeBrush } from "$lib/state/active-brush";
  import { scaleX, scaleY } from "$lib/state/scales";
  import { currentTransform } from "$lib/state/zoom";
  import type DataItem from "$lib/types/data-item";

  export let id: string;
  export let className: string;
  export let width: number;
  export let height: number;

  let brushCanvasElement: SVGElement;

  const dispatch = createEventDispatcher();

  const brushBehavior = brush()
    .keyModifiers(false)
    .filter((event) => (event.ctrlKey || event.shiftKey) && !event.button)
    .on("end", onBrushEnd);


  function onBrushEnd(event: D3BrushEvent<DataItem>) {
    const selection = event.selection;

    if (selection === null || selection === undefined) {
      $activeBrush = [
        [null, null],
        [null, null]
      ];
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

  onMount(() => {
    // use a timeout to ensure that the brush canvas has the right size when calling the brush
    // behavior
    setTimeout(() => {
      const brushSvg = select(brushCanvasElement);
      brushSvg.call(brushBehavior);
    }, 10);
  });
</script>

<svg
  id="{id}-brush-canvas"
  class="brush interaction-canvas {className}"
  {width}
  {height}
  on:mousemove={(e) => dispatch("hover", e)}
  on:click={(e) => dispatch("click", e)}
  bind:this={brushCanvasElement}
/>
