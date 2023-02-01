<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import VegaLitePlot from "./vega-lite-plot.svelte";

  export let id: string;
  export let colors: string[] = [];
  export let width = 100;
  export let height = 100;
  export let bins = 50;
  export let data: Record<string, unknown>[];
  export let dimension: string;
  export let domain: [number, number] = null;
  export let selectedInterval: [number, number] = null;
  export let usePresetInterval = true;
  export let groupDimension: string = null;
  export let showTitle = false;
  export let uncertainty: number = null;

  const dispatch = createEventDispatcher();

  function onBrush(event) {
    usePresetInterval = false;
    dispatch("interval", event.detail.value);
  }

  function onEnd() {
    dispatch("end");
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
    width: width,
    height: height,
    layer: [
      {
        mark: { type: "bar", tooltip: true },
        params: [
          {
            name: "brush",
            select: { type: "interval", encodings: ["x"] }
          }
        ],
        encoding: {
          x: {
            bin: { maxbins: bins },
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
        mark: { type: "bar", tooltip: true },
        transform: [{ filter: { param: "brush" } }],
        encoding: {
          x: {
            bin: { maxbins: bins },
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

  $: uncertaintyLayer = {
    mark: {
      type: "bar",
      tooltip: true,
      color: {
        gradient: "linear",
        x1: 1,
        y1: 1,
        x2: 1,
        y2: 0,
        stops: [
          {offset: 0, color: "rgba(255,255,255,1)"},
          {offset: 1 - uncertainty, color: "rgba(255,255,255,0)"},
        ]
      }
    },
    transform: [{ filter: { param: "brush" } }],
    encoding: {
      x: {
        bin: { maxbins: bins },
        field: { repeat: "repeat" }
      },
      y: {
        aggregate: "count",
        title: null
      }
    }
  };

  $: if (!showTitle) {
    histogram.layer[0].encoding.x["title"] = false;
  }
  $: if (domain !== null) {
    histogram.layer.forEach((l) => (l.encoding.x["scale"] = { domain }));
  }
  $: if (usePresetInterval && selectedInterval !== null && data) {
    histogram.layer[0].params[0]["value"] = { x: selectedInterval };
  }
  $: if (uncertainty !== null) {
    (histogram.layer as Record<string, unknown>[])[2] = uncertaintyLayer;
  } else {
    (histogram.layer as Record<string, unknown>[]).splice(2, 1);
    histogram = histogram;
  }
</script>

<VegaLitePlot {id} spec={histogram} on:brush={onBrush} on:end={onEnd} />
