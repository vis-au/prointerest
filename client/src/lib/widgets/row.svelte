<script lang="ts">
  export let id = "";
  export let width = -1;
  export let height = -1;
  export let style = "";

  const maxWidth = width === -1 ? "" : `max-width:${width}px;`;
  const maxHeight = height === -1 ? "" : `max-height:${width}px;`;
</script>

<div {id} class="row" style="{maxWidth}{maxHeight}{style}">
  <slot />
</div>

<style>
  div.row {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    flex-wrap: wrap;
  }
</style>
