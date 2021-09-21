<script>
  export let newTab = true;
  export let href = "#";
</script>

{#if newTab}
  <a {href} target="_blank" rel="noopener noreferrer">
    <slot />
  </a>
{:else}
  <a {href}>
    <slot />
  </a>
{/if}

<style>
  a {
    color: #333;
    text-decoration: underline;
    font-weight: bold;
  }
</style>
