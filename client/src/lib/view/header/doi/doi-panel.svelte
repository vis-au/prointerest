<script lang="typescript">
  import { selectedDoiWeight } from "$lib/state/selected-doi-weight";
  import ControlButton from "$lib/widgets/control-button.svelte";

  export let title: string;
  export let message = "";
</script>

<div class="doi-config">
  <h2>
    <span>{title}</span>
    <ControlButton on:click={() => ($selectedDoiWeight = null)}>close</ControlButton>
  </h2>
  {#if message.length > 0}
    <p class="message">{message}</p>
  {/if}
  <div class="content">
    <slot />
  </div>
</div>

<style>
  div.doi-config {
    background: white;
    padding: 1rem 1.5rem 2.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  div.doi-config h2 {
    margin: 10px 0;
    font-size: 15pt;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  div.content {
    border-top: 1px solid #efefef;
    padding-top: 20px;
    min-height: 150px;
    max-height: 550px;
    overflow: auto;
  }
</style>
