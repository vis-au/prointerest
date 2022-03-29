<script lang="ts">
  import BigNumber from "./big-number.svelte";

  export let values: string[];
  export let isOrdered = false;
  export let count = false;
  export let style = "";

  let countMap = new Map<string, number>();
  $: if (count) {
    countMap = new Map();
    values.forEach((value) =>
      countMap.has(value) ? countMap.set(value, countMap.get(value) + 1) : countMap.set(value, 1)
    );
  }
</script>

{#if isOrdered}
  <ol class="list" {style}>
    {#if count}
      {#each Array.from(countMap.keys()) as key}
        <li>{key}: <BigNumber>{countMap.get(key)}</BigNumber></li>
      {/each}
    {:else}
      {#each values as value}
        <li>{value}</li>
      {/each}
    {/if}
  </ol>
{:else}
  <ul class="list" {style}>
    {#if count}
      {#each Array.from(countMap.keys()) as key}
        <li>{key}: {countMap.get(key)}</li>
      {/each}
    {:else}
      {#each values as value}
        <li>{value}</li>
      {/each}
    {/if}
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
