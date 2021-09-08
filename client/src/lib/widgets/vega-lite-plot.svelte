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
      res.view.addSignalListener("brush", (name, value) => dispatch("brush", { value }));
    }, 0);
  });
</script>

<svelte:head>
  <script src="https://cdn.jsdelivr.net/npm/vega"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed"></script>
</svelte:head>

<div id="{id}-vega-container" />
