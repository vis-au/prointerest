<script lang="typescript">

export let title: string;
export let message = "";
export let width = -1;

const maxWidth = width < 0 ? "" : `max-width:${width}px`;

</script>

<div class="doi-config" style={maxWidth}>
  <h2>{ title }</h2>
  { #if message.length > 0 }
    <p class="message">{ message }</p>
  { /if }
  <slot></slot>
</div>

<style>
  div.doi-config {
    background: white;
    min-width: 300px;
    min-height: 150px;
    padding: 1rem 1.5rem 1.5rem;
    overflow: auto;
  }
  div.doi-config h2 {
    margin: 10px 0;
  }
</style>
