<script>
	import { dragInteractionModes } from '$lib/interaction/doi-interaction';
	import { activeIndicateMode } from '$lib/state/active-indicate-mode';
	import { activeInteractionMode } from '$lib/state/active-interaction-mode';
	import { activeViewMode } from '$lib/state/active-view-mode';
	import { indicationModes } from '$lib/types/indicate-mode';
	import { viewModes } from '$lib/types/view-modes';
	import Alternatives from '$lib/widgets/alternatives.svelte';
	import Row from '$lib/widgets/row.svelte';
</script>

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

<style>
	:global(#view-controls *)  {
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