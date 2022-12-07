<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import MiniHistogram from "./mini-histogram.svelte";
  import Slider from "./slider.svelte";

  export let id: string;
  export let label: string;
  export let width: number;
  export let sliderWidth = 0.3 * width;
  export let min: number;
  export let max: number;
  export let steps = 100;
  export let value: number;
  export let values: number[];
  export let updateLive = true;
  export let showValue = true;
  export let showDomain = true;
  export let style = "";

  $: sliderWidth = width * 0.45;

  const dispatch = createEventDispatcher();
</script>

<div class="histogram-slider">
  <Slider
    id="{id}-with-histogram"
    bind:label
    bind:width
    bind:sliderWidth
    bind:min
    bind:max
    bind:steps
    bind:value
    bind:updateLive
    bind:showValue
    bind:showDomain
    bind:style
    on:end={(event) => dispatch("end", event.detail)}
  >
    <MiniHistogram id="{id}-with-slider" width={sliderWidth} height={15} bind:values />
  </Slider>
</div>

<style>
</style>
