<script lang="ts">
  export let id = "";
  export let className = "";
  export let width = -1;
  export let height = -1;
  export let style = "";

  const maxWidth = width === -1 ? "0" : `${width}px;`;
  const maxHeight = height === -1 ? "0" : `${width}px;`;
</script>

<div {id} class="column {className}" style:maxWidth style:maxHeight {style}>
  <slot />
</div>

<style>
  div.column {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
</style>
