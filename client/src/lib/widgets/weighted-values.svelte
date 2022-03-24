<script lang="typescript">
  import { createEventDispatcher } from "svelte";
  import { isResizing } from "$lib/state/is-resizing";
  import type { ResizeEvent } from "$lib/types/resize-event";

  import Divider from "./divider.svelte";

  export let id: string;
  export let valueWeights: Map<string, number>;
  export let activeWeight: string = null;
  export let totalSize = 250;
  export let height = 28;
  export let showValue = false;
  export let weightsRemovable = false;
  export let useDarkmode = false;
  export let backgroundColor = "";
  export let isSelectable = true;

  $: weights = Array.from(valueWeights.entries());
  let resize: ResizeEvent;
  const dispatch = createEventDispatcher();

  function getId(key: string) {
    return `${key.split(" ").join("_")}-${id}`;
  }

  function selectWeight(weight: string) {
    if (activeWeight === weight) {
      activeWeight = null;
    } else {
      activeWeight = weight;
    }
  }

  function onWeightRemoved(weight: string) {
    dispatch("remove-weight", weight);
  }

  function onResizingStarted(event: ResizeEvent) {
    resize = event;
    $isResizing = event;
    document.addEventListener("mousemove", onResizing);
    document.addEventListener("mouseup", onResizingEnded);
    dispatch("start", resize);
  }

  function onResizing(event: MouseEvent) {
    const deltaX = event.movementX;

    const leftWeight = valueWeights.get(resize.leftId);
    const rightWeight = valueWeights.get(resize.rightId);
    const leftSize = leftWeight * totalSize;
    const rightSize = rightWeight * totalSize;

    let newLeftSize: number = leftSize;
    let newRightSize: number = rightSize;

    if (deltaX > 0) {
      if (rightSize === 0) {
        return;
      }

      // growing left and shrinking right
      newRightSize = Math.max(rightSize - deltaX, 0);
      newLeftSize = Math.min(leftSize + deltaX, leftSize + rightSize);
    } else {
      if (leftSize === 0) {
        return;
      }
      // shrinking left and growing right
      newLeftSize = Math.max(leftSize + deltaX, 0);
      newRightSize = Math.min(rightSize - deltaX, leftSize + rightSize);
    }

    const newLeftWeight = newLeftSize / totalSize;
    const newRightWeight = newRightSize / totalSize;

    valueWeights.set(resize.leftId, newLeftWeight);
    valueWeights.set(resize.rightId, newRightWeight);
    $isResizing.leftValue = newLeftWeight;
    $isResizing.rightValue = newRightWeight;

    valueWeights = new Map(valueWeights);
    dispatch("resizing", resize);
  }

  function onResizingEnded() {
    resize = null;
    $isResizing = null;
    document.removeEventListener("mousemove", onResizing);
    document.removeEventListener("mouseup", onResizingEnded);
    dispatch("end", resize);
  }
</script>

<div {id} class="weighted-values {useDarkmode ? 'dark' : ''}" style="height:{height}px">
  {#each weights as entry, i}
    <div
      class="entry {activeWeight === entry[0] ? 'active' : ''}"
      style="width:{entry[1] * totalSize}px;{backgroundColor.length > 0
        ? `background:${backgroundColor}`
        : ''}"
    >
      <label for={getId(entry[0])} title={`${entry[0]}: ${entry[1] * 100}%`}>
        <span class="key">{entry[0]}</span>
        {#if showValue}
          :
          <span class="value">{entry[1]}</span>
        {/if}
      </label>

      <input
        id={getId(entry[0])}
        type="radio"
        name={id}
        value={entry[0]}
        bind:group={activeWeight}
        on:click={() => isSelectable ? selectWeight(entry[0]): null}
      />
      {#if weightsRemovable}
        <button class="remove" on:click={() => onWeightRemoved(entry[0])}>x</button>
      {/if}
    </div>

    {#if i !== Array.from(valueWeights.entries()).length - 1}
      <Divider
        left={weights[i][0]}
        right={weights[i + 1][0]}
        isResizing={resize && resize.leftId == weights[i][0] && resize.rightId == weights[i + 1][0]}
        group={id}
        weights={valueWeights}
        on:resize-started={(e) => onResizingStarted(e.detail)}
      />
    {/if}
  {/each}
</div>

<style>
  div.weighted-values,
  div.entry,
  div.entry label {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: center;
  }

  div.entry {
    background: #efefef;
    border-radius: 4px;
    color: black;
    font-weight: bold;
    -moz-user-select: none;
    -webkit-user-select: none;
  }
  div.entry:hover {
    filter: brightness(0.9);
  }
  div.entry.active {
    filter: brightness(0.95);
    border: 3px solid black;
  }
  .dark div.entry {
    background: #555;
    color: #fff;
  }
  .dark div.entry:hover {
    filter: brightness(1.05);
  }
  .dark div.entry.active {
    filter: brightness(1.1);
    border: 3px solid white;
  }

  div.entry label {
    width: 100%;
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    align-items: center;
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

  div.entry button.remove {
    background: transparent;
    border: none;
    cursor: pointer;
    font-weight: bold;
    padding-right: 10px;
  }
  div.weighted-values.dark div.entry button.remove {
    color: white;
  }
</style>
