<script>
	import { dragInteractionModes } from '$lib/interaction/doi-interaction';
	import { activeSuggestionMode } from '$lib/state/active-indicate-mode';
	import { activeInteractionMode } from '$lib/state/active-interaction-mode';
	import { activeViewEncodings } from '$lib/state/active-view-encodings';
	import { activeViewMode } from '$lib/state/active-view-mode';
	import { dimensions } from '$lib/state/processed-data';
	import { suggestionModes } from '$lib/types/indicate-mode';
	import { viewModes } from '$lib/types/view-modes';
	import Alternatives from '$lib/widgets/alternatives.svelte';
	import Dropdown from '$lib/widgets/dropdown.svelte';
	import Row from '$lib/widgets/row.svelte';
</script>

<Row id="view-controls">
	<div class="configuration">
		<h2>View</h2>
		<Alternatives
			name="view-modes"
			alternatives={viewModes}
			bind:activeAlternative={$activeViewMode}
		/>
	</div>
	<div class="configuration">
		<h2>Axes</h2>
		<Dropdown id="x-encoding" className="encoding" bind:selectedValue={$activeViewEncodings.x}>
			{#each $dimensions as dim}
				<option>{dim}</option>
			{/each}
		</Dropdown>
		<Dropdown id="y-encoding" className="encoding" bind:selectedValue={$activeViewEncodings.y}>
			{#each $dimensions as dim}
				<option>{dim}</option>
			{/each}
		</Dropdown>
	</div>
	<div class="configuration">
		<h2>Suggestion</h2>
		<Alternatives
			name="suggestion-modes"
			alternatives={suggestionModes}
			bind:activeAlternative={$activeSuggestionMode}
		/>
	</div>
	<div class="configuration">
		<h2>Interaction</h2>
		<Alternatives
			name="interaction-modes"
			alternatives={dragInteractionModes}
			bind:activeAlternative={$activeInteractionMode}
		/>
	</div>
</Row>

<style>
	:global(#view-controls *) {
		font-size: 12pt;
	}

	:global(.show-me) {
		margin-left: 10px;
	}

	:global(div.configuration .encoding) {
		max-width: 150px;
		margin: 0 5px;
	}

	div.configuration {
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-right: 100px;
	}

	h2 {
		font-weight: normal;
		margin: 0;
		margin-right: 0.2rem;
		padding: 0;
	}
</style>
