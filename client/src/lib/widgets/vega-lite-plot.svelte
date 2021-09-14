<script lang="typescript">
  import { afterUpdate, createEventDispatcher } from "svelte";

  export let id: string;
  export let spec: Record<string, unknown>;

  const dispatch = createEventDispatcher();

  let vegaEmbed;

  afterUpdate(() => {
    // can happen on load
    if (Window === undefined) {
      return;
    }
    vegaEmbed = (window as Window)["vegaEmbed"];
    if (vegaEmbed === undefined) {
      console.error("vega embed is undefined");
      return;
    }

    setTimeout(async () => {
      const res = await vegaEmbed.embed(`#${id}-vega-container`, spec, { actions: false });
      res.view.addSignalListener("brush", (name: string, value: Record<string, unknown>) =>
        dispatch("brush", { value })
      );
    }, 10);
  });
</script>

<div id="{id}-vega-container" on:mouseup={() => dispatch("end")} />
