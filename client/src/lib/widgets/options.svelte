<script lang="typescript">
  import Dropdown from "./dropdown.svelte";

  export let id = "";
  export let className = "";
  export let style = "";
  export let options: string[];
  export let activeOptions: Record<string, boolean>;
  export let showInactive = true;
  export let showActive = true;

  $: inactiveOptions = options.filter((o) => !activeOptions[o]);
  $: activeOptionKeys = Object.keys(activeOptions).filter((o) => activeOptions[o]);

  function select(option: string) {
    activeOptions[option] = true;
    activeOptions = activeOptions;
  }
</script>

<div {id} class="options {className}" {style}>
  {#if showInactive}
    {#each options as option}
      <div class="option">
        <input
          id="options-list-{option}"
          type="checkbox"
          value={option}
          bind:checked={activeOptions[option]}
        />
        <label for="options-list-{option}">{option}</label>
      </div>
    {/each}
  {:else}
    <Dropdown id="inactive-options" selectedValue="null" style="margin-right:20px">
      <option disabled value="null">add ...</option>
      {#each inactiveOptions as option}
        <option value={option} on:click={() => select(option)}>{option}</option>
      {/each}
    </Dropdown>

    {#if showActive}
      {#each activeOptionKeys as option}
        <div class="option">
          <input
            id="options-list-{option}"
            type="checkbox"
            value={option}
            bind:checked={activeOptions[option]}
          />
          <label for="options-list-{option}">{option}</label>
        </div>
      {/each}
    {/if}
  {/if}
</div>

<style>
  div.options {
    display: flex;
    flex-flow: row wrap;
    line-height: 30px;
  }
  div.options div.option {
    margin-right: 15px;
  }
  div.options div.option input {
    display: none;
  }
  div.options div.option label {
    background: #efefef;
    cursor: pointer;
    border-radius: 4px;
    padding: 3px 10px;
  }
  div.options div.option input:checked + label {
    background: black;
    color: white;
  }
</style>
