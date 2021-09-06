<script lang="typescript">
  import { afterUpdate } from "svelte";
  import { axisBottom, axisLeft } from "d3-axis";
  import type { Selection } from "d3-selection";
  import { select } from "d3-selection";

  import { scaleX, scaleY } from "$lib/state/scales";
  import { currentTransform } from "$lib/state/zoom";

  export let width: number;
  export let height: number;
  let svg: SVGElement;

  $: xAxis = axisBottom($currentTransform.rescaleX($scaleX))
    .tickSize(height - 20);
  $: yAxis = axisLeft($currentTransform.rescaleY($scaleY))
    .tickSize(width - 20);

  function styleAxes(g: Selection<SVGGElement, unknown, null, undefined>) {
    g.select("path.domain").remove();
    g.selectAll(".tick line")
      .attr("stroke-opacity", 0.5)
      .attr("stroke-dasharray", "2,2");
  }

  afterUpdate(() => {
    const canvas = select(svg);
    canvas.selectAll("*").remove();
    canvas.append("g")
      .attr("class", "axis x")
      .call(xAxis)
      .call(styleAxes);
    canvas.append("g")
      .attr("class", "axis y")
      .attr("transform", `translate(${width},0)`)
      .call(yAxis)
      .call(styleAxes);
  });

</script>


<svg bind:this={svg} id="axes" { width } { height }></svg>


<style>
  svg#axes {
    position: absolute;
  }
</style>