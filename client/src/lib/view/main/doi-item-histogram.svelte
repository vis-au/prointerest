<script lang="ts">
  import type DataItem from "$lib/types/data-item";
  import { dataItemToRecord } from "$lib/util/item-transform";
  import Histogram from "$lib/widgets/histogram.svelte";
  import { createEventDispatcher } from "svelte";

  export let id: string;
  export let colors: string[] = [];
  export let width = 100;
  export let height = 100;
  export let bins = 50;
  export let data: DataItem[];
  export let dimension: string;
  export let domain: [number, number] = null;
  export let selectedInterval: [number, number] = null;
  export let usePresetInterval = true;
  export let groupDimension: string = null;
  export let showTitle = false;

  const dispatch = createEventDispatcher();

  $: tabularData = data.map(dataItemToRecord);
</script>

<Histogram
  bind:id
  bind:colors
  bind:width
  bind:height
  bind:bins
  data={tabularData}
  bind:dimension
  bind:domain
  bind:selectedInterval
  bind:usePresetInterval
  bind:groupDimension
  bind:showTitle
  on:end={() => dispatch("end")}
  on:interval={(event) => dispatch("interval", event.detail)}
/>
