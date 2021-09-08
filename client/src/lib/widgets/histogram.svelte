<script lang="typescript">
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
    mark: "bar",
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
  };

  $: showTitle ? "" : (histogram.encoding.x["title"] = false);
</script>

<VegaLitePlot {id} spec={histogram} />
