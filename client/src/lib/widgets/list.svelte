<script lang="typescript">
  export let values: string[];
  export let isOrdered = false;
  export let style = "";
</script>

{#if isOrdered}
  <ol class="list" {style}>
    {#each values as value}
      <li>{value}</li>
    {/each}
  </ol>
{:else}
  <ul class="list" {style}>
    {#each values as value}
      <li>{value}</li>
    {/each}
  </ul>
{/if}

<style>
  .list {
    display: flex;
    flex-direction: row;
    justify-content: start;
    flex-wrap: wrap;
    margin: 0;
    padding: 0;
  }
  li {
    list-style-position: inside;
    padding: 2px 5px;
    border: 1px solid #ccc;
    border-radius: 3px;
    margin: 3px 5px;
  }
  ul li {
    list-style: none;
  }
  ol li::before {
    color: red;
  }
</style>