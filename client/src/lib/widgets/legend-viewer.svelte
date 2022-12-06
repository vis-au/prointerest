<script lang="ts">
  import { range } from "d3-array";
  import type { ScaleDiverging, ScaleSequential } from "d3-scale";
  import { scaleLinear } from "d3-scale";

  export let id: string;
  export let color: ScaleSequential<string, never> | ScaleDiverging<string, never>;
  export let title: string;
  export let left = 0;
  export let top = 0;
  export let width = 200;
  export let height = 25;
  export let margin = 3;
  export let blockSize: number;
  export let steps = 10;
  export let isVertical = false;

  const segmentWidth = width / (steps + 1);
  $: scaleX = scaleLinear()
    .domain([0, steps])
    .range([margin, width - margin]);

  $: scaleY = scaleLinear()
    .domain([0, steps])
    .range([margin, height - margin]);

  $: domain = color.domain();
  $: values = range(
    domain[0],
    domain[domain.length - 1],
    Math.abs(domain[0] - domain[domain.length - 1]) / steps
  );
</script>

<svg
  id="{id}-legend-canvas"
  class="legend"
  {width}
  {height}
  style:left="{left}px"
  style:top="{top}px">
  <g class="color">
    <text class="legend-title" x={margin} y={margin}>{title}</text>
    <g class="values" transform="translate(0,{22})">
      {#each values as value, i}
        <rect
          class="value"
          width={segmentWidth}
          height={blockSize}
          x={isVertical ? 0 : scaleX(i)}
          y={isVertical ? scaleY(i) : 0}
          fill={color(value)}
        />
      {/each}
    </g>
    <g class="label left" transform="translate({margin},{blockSize + margin + 5})">
      <rect width="30" height="14" />
      <text class="low">{id === "center" ? "> left" : "low"}</text>
    </g>
    <g class="label right" transform="translate({width - margin},{blockSize + margin + 5})">
      <rect x={-30} width="30" height="14" />
      <text class="high">{id === "center" ? "> right" : "high"}</text>
    </g>
  </g>
</svg>

<style>
  svg.legend {
    position: absolute;
    background: rgba(255, 255, 255, 0.73);
    shape-rendering: crispEdges;
  }

  svg.legend rect.value {
    stroke: white;
    stroke-width: 0.25px;
  }

  svg.legend g.color g.label rect {
    fill: rgba(255, 255, 255, 0.7);
  }

  svg.legend text {
    fill: black;
    font-size: 15px;
    transform: translateY(15px);
  }
  svg.legend text.legend-title {
    font-weight: bold;
  }
  svg.legend text.high {
    text-anchor: end;
  }

  svg.legend g.color-scheme rect {
    cursor: pointer;
  }
</style>
