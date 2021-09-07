<script lang="typescript">
  export let name: string;
  export let alternatives: string[];
  export let activeAlternative: string;
</script>

<div id="{name}-alternatives" class="alternatives">
  {#each alternatives as alternative}
    <label
      for="{alternative.split(' ').join('_')}-{name}-alternative"
      class="alternative {alternative === activeAlternative ? 'active' : ''}"
      title={alternative}
    >
      <div class="alternative-text {alternative === activeAlternative ? 'active' : ''}">
        {alternative}
      </div>
      <input
        id="{alternative.split(' ').join('_')}-{name}-alternative"
        type="radio"
        {name}
        value={alternative}
        bind:group={activeAlternative}
      />
    </label>
  {/each}
</div>

<style>
  div.alternatives {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  div.alternatives .alternative {
    margin-left: 10px;
  }

  div.alternatives div.alternative-text {
    font-family: sans-serif;
    background: #efefef;
    color: black;
    border-color: #efefef;
    padding: 2px 15px 1.5px;
    border-radius: 20px;
    cursor: pointer;
  }
  div.alternatives div.alternative-text:hover {
    background: #ddd;
  }
  div.alternatives div.alternative-text.active {
    background: black;
    color: white;
    text-decoration: none;
  }
  div.alternatives input[type="radio"] {
    display: none;
  }
</style>
