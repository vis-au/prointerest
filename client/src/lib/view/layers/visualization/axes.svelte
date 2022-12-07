<script lang="ts">
  import { afterUpdate } from "svelte";
  import { axisBottom, axisLeft } from "d3-axis";
  import type { Selection } from "d3-selection";
  import { select } from "d3-selection";

  import { scaleX, scaleY } from "$lib/state/scales";
  import { currentTransform } from "$lib/state/zoom";
  import { activeViewEncodings } from "$lib/state/active-view-encodings";

  export let width: number;
  export let height: number;
  let container: SVGGElement;

  $: xAxis = axisBottom($currentTransform.rescaleX($scaleX)).tickSize(height - 20);
  $: yAxis = axisLeft($currentTransform.rescaleY($scaleY)).tickSize(width - 35);

  function styleAxes(g: Selection<SVGGElement, unknown, null, undefined>) {
    g.select("path.domain").remove();
    g.selectAll(".tick line").attr("stroke-opacity", 0.5).attr("stroke-dasharray", "2,2");
  }

  afterUpdate(() => {
    const canvas = select(container);
    canvas.selectAll("g.axis").remove();
    canvas.append("g").attr("class", "axis x").call(xAxis).call(styleAxes);
    canvas
      .append("g")
      .attr("class", "axis y")
      .attr("transform", `translate(${width},0)`)
      .call(yAxis)
      .call(styleAxes);
  });
</script>

<svg id="axes" {width} {height}>
  <g bind:this={container} id="axes-container" />
  <rect
    class="background x"
    x={width / 2}
    y={height - 2}
    width={150}
    height={20}
    transform="translate(-75,-16)"
  />
  <text class="label x" transform="translate({width / 2},{height - 2})">
    {$activeViewEncodings.x}
  </text>
  <rect
    class="background y"
    x={0}
    y={height / 2}
    width={20}
    height={150}
    transform="translate(0,-75)"
  />
  <text class="label y" transform="translate({2},{height / 2})rotate(90)">
    {$activeViewEncodings.y}
  </text>
</svg>

<style>
  svg#axes {
    position: absolute;
  }
  text.label {
    text-anchor: middle;
  }
  rect.background {
    fill: rgba(255, 255, 255, 0.5);
  }
</style>
