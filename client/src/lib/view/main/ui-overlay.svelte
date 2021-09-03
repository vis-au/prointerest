<script lang="typescript">
	import { dragInteractionModes } from '$lib/interaction/doi-interaction';
	import { activeIndicateMode } from '$lib/state/active-indicate-mode';
	import { activeInteractionMode } from '$lib/state/active-interaction-mode';
	import { activeViewMode } from '$lib/state/active-view-mode';
	import { indicationModes } from '$lib/types/indicate-mode';
	import { viewModes } from '$lib/types/view-modes';
	import Alternatives from '$lib/widgets/alternatives.svelte';
	import Minimap from '$lib/view/main/minimap.svelte';
	import Row from '$lib/widgets/row.svelte';

	export let visible: boolean;
	export let width: number;
	export let height: number;
</script>

<div class="ui-overlay {visible ? '' : 'hidden'}" style="width:{width}px">
	<Row id="view-controls">
		<div class="mode-selection">
			<h2>View</h2>
			<Alternatives
				name="view-modes"
				alternatives={viewModes}
				bind:activeAlternative={$activeViewMode}
			/>
		</div>
		<div class="mode-selection">
			<h2>Guidance</h2>
			<Alternatives
				name="guidance-modes"
				alternatives={indicationModes}
				bind:activeAlternative={$activeIndicateMode}
			/>
		</div>
		<div class="mode-selection">
			<h2>Interaction</h2>
			<Alternatives
				name="interaction-modes"
				alternatives={dragInteractionModes}
				bind:activeAlternative={$activeInteractionMode}
			/>
		</div>
	</Row>
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
	div.ui-overlay * {
		font-size: 12pt;
	}

	div.mode-selection {
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-right: 100px;
	}

	div.mode-selection h2 {
		font-weight: normal;
		margin: 0;
		margin-right: 0.2rem;
		padding: 0;
	}
</style>
