<script>
  export let style = "";
</script>

<span class="big-number" {style}>
  <slot />
</span>

<style>
  span.big-number {
    text-align: center;
    background: red;
    padding: 2px 5px;
    background: #efefef;
    border-radius: 4px;
    font-weight: bold;
  }
</style>
