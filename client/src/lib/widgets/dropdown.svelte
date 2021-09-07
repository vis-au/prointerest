<script lang="typescript">
  export let id: string;
  export let className = "";
  export let selectedValue: string;
  export let style = "";
</script>

<label for={id} class="dropdown {className}">
  <select name={id} {id} bind:value={selectedValue} {style}>
    <slot />
  </select>

  <svg>
    <polyline points="1 1 5 5 9 1" />
  </svg>
</label>

<style>
  label.dropdown {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
  }
  label.dropdown select {
    -webkit-appearance: none;
    padding: 4px 40px 4px 12px;
    width: 100%;
    border: 1px solid #e8eaed;
    border-radius: 5px;
    background: white;
    box-shadow: 0 1px 3px -2px #aaa;
    cursor: pointer;
    font-family: inherit;
    font-size: 14px;
    transition: all 150ms ease;
  }
  label.dropdown select:required:invalid {
    color: #5a667f;
  }
  label.dropdown select:hover + svg {
    stroke: black;
  }
  label.dropdown svg {
    position: absolute;
    right: 10px;
    top: 13px;
    width: 10px;
    height: 6px;
    stroke-width: 2px;
    stroke: #aaa;
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
    pointer-events: none;
  }
</style>
