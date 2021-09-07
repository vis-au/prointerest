<script lang="typescript">
	import { createEventDispatcher } from 'svelte';

	export let id = '';
	export let className = '';
	export let style = '';

	const dispatch = createEventDispatcher();

	function click() {
		dispatch('click');
	}
</script>

<button {id} class="control-button {className}" on:click={click} {style}>
	<slot />
</button>

<style>
	button.control-button {
		background: #333;
		color: white;
		cursor: pointer;
		border: none;
		border-radius: 3px;
		font-size: 12pt;
	}
</style>
