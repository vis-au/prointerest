<script lang="typescript">

export let id = "";
export let width = -1;
export let height = -1;

const maxWidth = width === -1 ? "" : `max-width:${width}px;`;
const maxHeight = height === -1 ? "" : `max-height:${width}px;`;

</script>

<div id={ id } class="column" style="{maxWidth}{maxHeight}">
  <slot></slot>
</div>

<style>
  div.column {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
</style>