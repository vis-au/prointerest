<script lang="typescript">
  export let id = "";
  export let className = "";
  export let style = "";
  export let options: string[];
  export let activeOptions: Record<string, boolean>;
</script>

<div {id} class="options {className}" {style}>
  {#each options as option}
    <div class="option">
      <input
        id="options-list-{option}"
        type="checkbox"
        value={option}
        bind:checked={ activeOptions[option] }
      />
      <label for="options-list-{option}">{option}</label>
    </div>
  {/each}
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