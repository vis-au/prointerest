<script lang="typescript">

export let group: string;
export let valueWeights: Map<string, number>;
export let activeWeight: string = null;
export let totalSize = 250;
export let showValue = false;

function getId(key: string) {
  return `${key.split(" ").join("_")}-${group}`;
}

function selectWeight(weight: string) {
  console.log(activeWeight, weight);
  if (activeWeight === weight) {
    activeWeight = null;
  } else {
    activeWeight = weight;
  }
}

</script>


<div id={ group } class="weighted-values">
  { #each Array.from(valueWeights.entries()) as entry, i }
    <div
      class="entry {activeWeight === entry[0] ? "active" : ""}"
      style="width:{ entry[1] * totalSize}px">

      <label for={ getId(entry[0]) } title={ `${entry[0]}: ${entry[1] * 100}%` }>
        <span class="key">{ entry[0] }</span>
        { #if showValue }
          :
          <span class="value">{ entry[1] }</span>
        { /if }
      </label>

      <input
        id={ getId(entry[0]) }
        type="radio"
        name={ group }
        value={ entry[0] }
        bind:group={ activeWeight }
        on:click={ () => selectWeight(entry[0]) }
      />
    </div>

    { #if i !== Array.from(valueWeights.entries()).length-1 }
      <div class="divider"></div>
    { /if }
  { /each }
</div>


<style>
  div.weighted-values,
  div.entry,
  div.entry label {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
  }

  div.entry {
    background: #efefef;
    border-radius: 4px;
    -moz-user-select: none;
    -webkit-user-select: none;
  }
  div.entry:hover {
    background: #ddd;
  }
  div.entry.active {
    background: black;
    color: white;
  }

  div.entry label {
    width: 100%;
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  div.entry label .key {
    margin-right: 0.25rem;
  }
  div.entry label .value {
    font-weight: bold;
  }

  div.entry input {
    display: none;
  }

  div.divider {
    min-width: 0.5rem;
    min-height: 12px;
    cursor: w-resize;
  }
  div.divider:hover {
    background: #ccc;
  }
</style>