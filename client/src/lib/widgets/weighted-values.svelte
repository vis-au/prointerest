<script lang="typescript">
	import type { ResizeEvent } from "$lib/types/resize-event";

	import Divider from "./divider.svelte";

	export let group: string;
	export let valueWeights: Map<string, number>;
	export let activeWeight: string = null;
	export let totalSize = 250;
	export let showValue = false;

	$: weights = Array.from(valueWeights.entries());
	let resize: ResizeEvent;

	function getId(key: string) {
		return `${key.split(' ').join('_')}-${group}`;
	}

	function selectWeight(weight: string) {
		console.log(activeWeight, weight);
		if (activeWeight === weight) {
			activeWeight = null;
		} else {
			activeWeight = weight;
		}
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
			// growing left and shrinking right
			newRightSize = Math.max(rightSize - deltaX, 0);
			if (newRightSize > 0) {
				newLeftSize = leftSize + deltaX
			}
		} else {
			// shrinking left and growing right
			newLeftSize = Math.max(leftSize + deltaX, 0);
			if (newLeftSize > 0) {
				newRightSize = rightSize - deltaX
			}
		}

		const newLeftWeight = newLeftSize / totalSize;
		const newRightWeight = newRightSize / totalSize;

		valueWeights.set(resize.leftId, newLeftWeight);
		valueWeights.set(resize.rightId, newRightWeight);
		valueWeights = new Map(valueWeights);
	}

	function onResizingEnded() {
		resize = null;
		document.removeEventListener("mousemove", onResizing);
		document.removeEventListener("mouseup", onResizingEnded);
	}

	function onResizingStarted(event: ResizeEvent) {
		resize = event;
		document.addEventListener("mousemove", onResizing);
		document.addEventListener("mouseup", onResizingEnded);
	}
</script>

<div id={group} class="weighted-values">
	{#each weights as entry, i}
		<div
			class="entry {activeWeight === entry[0] ? 'active' : ''}"
			style="width:{entry[1] * totalSize}px"
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
				name={group}
				value={entry[0]}
				bind:group={activeWeight}
				on:click={() => selectWeight(entry[0])}
			/>
		</div>

		{#if i !== Array.from(valueWeights.entries()).length - 1}
			<Divider
				left={ weights[i][0] }
				right={ weights[i+1][0] }
				isResizing={ resize && resize.leftId==weights[i][0] && resize.rightId==weights[i+1][0] }
				{ group }
				on:resize-started={ (e) => onResizingStarted(e.detail) }
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
</style>
