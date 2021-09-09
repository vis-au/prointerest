<script lang="typescript">
  import { afterUpdate, createEventDispatcher } from "svelte";

  export let id: string;
  export let spec: Record<string, unknown>;

  const dispatch = createEventDispatcher();

  let vegaEmbed;

  afterUpdate(() => {
    vegaEmbed = (window as any).vegaEmbed;
    if (vegaEmbed === undefined) {
      console.error("vega embed is undefined");
      return;
    }

    setTimeout(async () => {
      const res = await vegaEmbed.embed(`#${id}-vega-container`, spec, { actions: false });
      res.view.addSignalListener("brush", (name: string, value: Record<string, unknown>) => dispatch("brush", { value }));
    }, 0);
  });
</script>

<svelte:head>
  <script src="static/scripts/vega.js"></script>
  <script src="static/scripts/vega-lite.js"></script>
  <script src="static/scripts/vega-embed.js"></script>
</svelte:head>

<div id="{id}-vega-container" />
