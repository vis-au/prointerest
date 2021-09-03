<script lang="typescript">
  export let id: string;
  export let selectedValue: string;
  export let style = "";
</script>

<label for={ id } class="dropdown">
  <select name={ id } id={ id } bind:value={ selectedValue } style={ style }>
    <slot></slot>
  </select>

  <svg>
    <use xlink-href="#select-arrow-down"></use>
  </svg>
</label>

<style>
  label.dropdown select {
  -webkit-appearance: none;
  padding: 7px 40px 7px 12px;
  width: 100%;
  border: 1px solid #E8EAED;
  border-radius: 5px;
  background: white;
  box-shadow: 0 1px 3px -2px #aaa;
  cursor: pointer;
  font-family: inherit;
  font-size: 14px;
  transition: all 150ms ease;
}
label.dropdown select:required:invalid {
  color: #5A667F;
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

:global(#sprites) {
  position: absolute;
  width: 0;
  height: 0;
  pointer-events: none;
  user-select: none;
}
</style>