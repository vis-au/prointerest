<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import VegaLitePlot from "./vega-lite-plot.svelte";

  export let id: string;
  export let colors: string[] = null;
  export let width: number;
  export let height: number;
  export let bins = 50;
  export let data: Record<string, unknown>[];
  export let transform: Record<string, unknown>[] = [];
  export let dimensions: string[];
  export let brushedInterval: Record<string, [number, number]> = null;
  export let usePresetInterval = true;
  export let groupDimension: string = null;
  export let showTitle = false;
  export let useLogScale = false;
  export let uncertainty: number = null;

  const dispatch = createEventDispatcher();
  const POINT_COLOR = "#555";

  $: brushedDimension =
    brushedInterval && Object.keys(brushedInterval).length > 0
      ? Object.keys(brushedInterval)[0]
      : null;

  let dataSize = data.length;
  $: {
    if (dataSize !== data.length) {
      usePresetInterval = true;
      dataSize = data.length;
    }
  }

  function onBrush(event: CustomEvent) {
    brushedInterval = event.detail.value;
    usePresetInterval = false;
    dispatch("interval", event.detail.value);
  }

  function onBrushEnd() {
    dispatch("end", brushedInterval);
  }

  let colorEncoding: Record<string, unknown> = {};

  $: if (colors && groupDimension) {
    colorEncoding = {
      field: groupDimension,
      legend: null,
      scale: { range: colors }
    };
  } else if (groupDimension === null && colors) {
    colorEncoding = {
      value: colors[0]
    };
  } else if (groupDimension) {
    colorEncoding = {
      value: POINT_COLOR
    };
  }

  $: histogram = {
    $schema: "https://vega.github.io/schema/vega-lite/v5.1.1.json",
    data: {
      values: data
    },
    transform: transform,
    repeat: dimensions,
    spec: {
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
              field: { repeat: "repeat" }
            },
            y: {
              aggregate: "count",
              title: null,
              scale: { type: useLogScale ? "symlog" : "linear" }
            },
            color: { value: "#ddd" }
          }
        },
        {
          mark: { type: "bar", tooltip: true },
          transform: [{ filter: { param: "brush" } }],
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
          {offset: uncertainty, color: "rgba(255,255,255,0)"},
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

  $: if (showTitle) {
    histogram.spec.layer[1].encoding.x["title"] = false;
  }
  $: if (usePresetInterval && brushedInterval && brushedDimension && data) {
    // histogram.spec.layer[0].params[0]["value"] = { x: brushedInterval[brushedDimension] };
    // FIXME: the code below does not work, as it seems to be a bug in vega-lite
    // https://github.com/vega/vega-lite/issues/8348
    // view?.signal("brush", {"trip_distance": [12.706451612903226,20.129032258064516]}).run();
  }
  $: if (uncertainty !== null) {
    (histogram.spec.layer as Record<string, unknown>[])[2] = uncertaintyLayer;
  } else {
    (histogram.spec.layer as Record<string, unknown>[]).splice(2, 1);
    histogram = histogram;
  }
</script>

<VegaLitePlot {id} spec={histogram} on:brush={onBrush} on:end={onBrushEnd} />
