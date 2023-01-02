<script lang="ts">
  import ControlButton from "../../widgets/control-button.svelte";

  export let x = 0;
  export let y = 0;
  export let label: string;
  export let active = true;

  let isHidden = true; // flag for whether the tree is visible or not

  function hide() {
    isHidden = true;
  }

  function show() {
    isHidden = false;
  }
</script>

<div
  class="view-panel"
  class:active
  style:left="{x}px"
  style:top="{y}px">

  {#if isHidden}
    <ControlButton id="toggle-dt-panel" style="width:2rem;height:2rem" on:click={show}
      >{label}</ControlButton
    >
  {:else}
    <div class="container">
      <h2>
        <slot class="left" name="header" />

        <div class="right">
          <ControlButton on:click={hide} style="width:20px;height:20px;line-height:20px;padding:0">
            <div style="transform:rotate(45deg)">+</div>
          </ControlButton>
        </div>
      </h2>

      <slot name="body" />
    </div>
  {/if}
</div>

<style>
  .view-panel {
    position: absolute;
    font-size: 12px;
  }
  .view-panel.active {
    border: 1px solid orange;
  }
  .view-panel h2 {
    display: flex;
    font-size: 14px;
    font-weight: normal;
    line-height: 1;
    margin: 0;
    margin-bottom: 15px;
    padding: 0;
    justify-content: space-between;
    align-items: center;
  }
  .view-panel h2 .left,
  .view-panel h2 .right {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
  }
  .view-panel h2 .left {
    margin-right: 25px;
  }
  .view-panel .container {
    background: white;
    border: 1px solid #e8eaed;
    box-shadow: 0 1px 3px -2px #aaa;
    border-radius: 4px;
    padding: 1rem;
  }
</style>
