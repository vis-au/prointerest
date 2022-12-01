<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import VegaLitePlot from "./vega-lite-plot.svelte";

  export let id: string;
  export let colors: string[] = [];
  export let width: number;
  export let height: number;
  export let bins = 50;
  export let data: Record<string, unknown>[];
  export let dimensions: string[];
  export let brushedInterval: Record<string, [number, number]> = null;
  export let usePresetInterval = true;
  export let groupDimension: string = null;
  export let showTitle = false;

  const dispatch = createEventDispatcher();

  $: brushedDimension = brushedInterval && Object.keys(brushedInterval).length > 0
    ? Object.keys(brushedInterval)[0]
    : null;


  function onBrush(event: CustomEvent) {
    usePresetInterval = false;
    brushedInterval = event.detail.value;
    dispatch("interval", event.detail.value);
  }

  function onBrushEnd() {
    dispatch("end", brushedInterval);
  }

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
    $schema: "https://vega.github.io/schema/vega-lite/v5.1.1.json",
    data: {
      values: data
    },
    repeat: dimensions,
    spec: {
      width: width,
      height: height,
      layer: [
        {
          params: [
            {
              name: "brush",
              select: { type: "interval", encodings: ["x"] }
            }
          ],
          mark: { type: "bar", tooltip: true },
          encoding: {
            x: {
              bin: { maxbins: bins },
              field: { repeat: "repeat" }
            },
            y: {
              aggregate: "count",
              title: null
            },
            color: { value: "#ddd" }
          }
        },
        {
          transform: [{ filter: { param: "brush" } }],
          mark: { type: "bar", tooltip: true },
          encoding: {
            x: {
              bin: { maxbins: bins },
              field: { repeat: "repeat" }
            },
            y: {
              aggregate: "count",
              title: null
            },
            color: colorEncoding
          }
        }
      ]
    }
  };

  $: if (showTitle) {
    histogram.spec.layer[1].encoding.x["title"] = false;
  }
  $: if (usePresetInterval && brushedInterval !== null && data) {
    histogram.spec.layer[0].params[0]["value"] = { x: brushedInterval[brushedDimension] };
  }
</script>

<VegaLitePlot {id} spec={histogram} on:brush={onBrush} on:end={onBrushEnd} />
