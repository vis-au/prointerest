<script lang="ts">
  import { range } from "d3-array";
  import type { ScaleDiverging, ScaleSequential } from "d3-scale";
  import { scaleSequential, scaleSequentialLog } from "d3-scale";
  import { scaleLinear } from "d3-scale";
  import { colorScaleTypes, divergingSchemes, sequentialSchemes } from "$lib/types/color";
  import { colorScaleType, colorScheme } from "$lib/state/active-color-scale";

  export let id: string;
  export let colorScale: ScaleSequential<string, never> | ScaleDiverging<string, never>;
  export let title: string = null;
  export let x: number;
  export let y: number;
  export let width = 225;
  export let height = 55;
  export let margin = 3;
  export let blockSize: number;
  export let steps = 10;
  export let isVertical = false;

  $: colorScale =
    $colorScaleType === "linear" ? scaleSequential($colorScheme) : scaleSequentialLog($colorScheme);

  $: scaleX = scaleLinear()
    .domain([0, steps])
    .range([margin, width - margin]);

  $: scaleY = scaleLinear()
    .domain([0, steps])
    .range([margin, height - margin]);

  $: segmentWidth = width / (steps + 1);
  $: domain = colorScale.domain();
  $: values = range(
    domain[0],
    domain[domain.length - 1],
    Math.abs(domain[0] - domain[domain.length - 1]) / steps
  );
</script>

<svg id="{id}-legend-canvas" class="legend" {width} {height} style:left="{x}px" style:top="{y}px">
  {#if title !== null}
    <text class="legend-title" x={margin} y={margin}>{title}</text>
  {/if}
  <g class="color" transform="translate(0,{title !== null ? 22 : 0})">
    <g class="values">
      {#each values as value, i}
        <rect
          class="value"
          width={segmentWidth}
          height={blockSize}
          x={isVertical ? 0 : scaleX(i)}
          y={isVertical ? scaleY(i) : 0}
          fill={colorScale(value)}
        />
      {/each}
    </g>
    <g class="label left" transform="translate({margin},-3)">
      <rect width="30" height="14" />
      <text class="low">{id === "center" ? "> left" : "low"}</text>
    </g>
    <g class="label right" transform="translate({width - margin},-3)">
      <rect x={-30} width="30" height="14" />
      <text class="high">{id === "center" ? "> right" : "high"}</text>
    </g>
  </g>
  <g
    class="scale-type"
    transform="translate({width - colorScaleTypes.length * 15 + margin},{height - 5 - margin})"
  >
    {#each colorScaleTypes as type, index}
      <circle
        class="scale-type-toggle"
        cx={index * 15}
        cy="0"
        r="5"
        fill={$colorScaleType === type ? "black" : "white"}
        stroke="black"
        on:click={() => ($colorScaleType = type)}
      >
        <title>{type}</title>
      </circle>
    {/each}
  </g>
  <g class="color-scheme" transform="translate({margin},{height - 12 - margin})">
    {#if id === "center"}
      {#each divergingSchemes as scheme, index}
        <rect
          x={index * 12}
          y={0}
          width={8}
          height={8}
          fill={$colorScheme === scheme ? "black" : "white"}
          stroke="black"
          on:click={() => ($colorScheme = scheme)}
        />
      {/each}
    {:else}
      {#each sequentialSchemes as scheme, index}
        <rect
          x={index * 12}
          y={0}
          width={8}
          height={8}
          fill={$colorScheme === scheme ? "black" : "white"}
          stroke="black"
          on:click={() => ($colorScheme = scheme)}
        />
      {/each}
    {/if}
  </g>
</svg>

<style>
  svg.legend {
    position: absolute;
    background: rgba(255, 255, 255, 0.73);
    shape-rendering: crispEdges;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
  svg.legend * {
    user-select: none;
    -moz-user-select: none;
    -webkit-user-select: none;
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

  svg.legend .scale-type circle.scale-type-toggle {
    cursor: pointer;
  }

  svg.legend g.color-scheme rect {
    cursor: pointer;
  }
</style>
