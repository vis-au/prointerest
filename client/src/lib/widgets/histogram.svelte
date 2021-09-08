<script lang="typescript">
import { createEventDispatcher } from "svelte";

  import VegaLitePlot from "./vega-lite-plot.svelte";

  export let id: string;
  export let colors: string[] = [];
  export let width = 100;
  export let height = 100;
  export let bins = 50;
  export let data: Record<string, unknown>[];
  export let dimension: string;
  export let groupDimension: string = null;
  export let showTitle = false;

  const dispatch = createEventDispatcher();

  $: colorEncoding =
    groupDimension === null
      ? {
          value: colors.length ? colors[0] : "#555"
        }
      : {
          field: groupDimension,
          legend: null,
          scale: {
            range: colors.length ? colors : ["teal", "orange"]
          }
        };

  $: histogram = {
    $schema: "https://vega.github.io/schema/vega-lite/v5.1.0.json",
    data: {
      values: data
    },
    width: width,
    height: height,
    layer: [
      {
        mark: "bar",
        params: [{
          name: "brush",
          select: {type: "interval", encodings: ["x"]}
        }],
        encoding: {
          x: {
            bin: {maxbins: bins},
            field: dimension
          },
          y: {
            aggregate: "count",
            title: null
          },
          color: colorEncoding
        }
      },
      {
        mark: "bar",
        transform: [{filter: {param: "brush"}}],
        encoding: {
          x: {
            bin: {maxbins: bins},
            field: dimension
          },
          y: {
            aggregate: "count",
            title: null
          },
          color: colorEncoding
        }
      }
    ]
  };

  $: showTitle ? "" : (histogram.layer[0].encoding.x["title"] = false);
</script>

<VegaLitePlot {id} spec={histogram} on:brush={ (event) => dispatch("interval", event.detail.value) } />
