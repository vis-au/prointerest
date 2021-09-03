<script lang="typescript">
	import Minimap from '$lib/view/main/minimap.svelte';
	import ViewControls from './view-controls.svelte';

	export let visible: boolean;
	export let width: number;
	export let height: number;
</script>

<div class="ui-overlay {visible ? '' : 'hidden'}" style="width:{width}px">
	<ViewControls />
	<Minimap />
</div>

<style>
	:global(div#view-controls) {
		box-sizing: border-box;
		justify-content: center;
		padding-top: 20px;
		width: 100%;
		background: rgba(255, 255, 255, 0.73);
		padding: 5px 30px;
		border-radius: 4px;
	}

	div.ui-overlay {
		box-sizing: border-box;
		position: absolute;
		transition: opacity 0.25s ease-in-out;
	}
	div.ui-overlay.hidden {
		visibility: hidden;
		opacity: 0;
	}
</style>
