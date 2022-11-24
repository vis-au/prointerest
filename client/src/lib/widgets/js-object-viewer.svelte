<script lang="ts">
  export let width = 1000;
  export let height = 1200;
  export let input: Record<string, unknown> | Record<string, unknown>[];
  export let style = "";
</script>

<div class="js-object-viewer" {style}>
  <pre style="max-width:{width}px;max-height:{height}px">{ JSON.stringify(input, null, 4) }</pre>
</div>

<style>
  .js-object-viewer {
    background: white;
    border: 1px solid #e8eaed;
    box-shadow: 0 1px 3px -2px #aaa;
    border-radius: 4px;
    padding: 1rem;
  }
  .js-object-viewer pre {
    border: 1px solid #e8eaed;
    padding: 0;
    margin: 0;
    margin-top: 0.5rem;
    line-height: 150%;
    overflow: auto;
  }
</style>