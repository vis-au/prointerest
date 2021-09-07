<script lang="typescript">
	import { colorScale } from '$lib/state/active-color-scale';
	import { activeViewMode } from '$lib/state/active-view-mode';
	import BrushLayer from '../layers/interaction/brushed-regions-layer.svelte';
	import InteractionLayer from '../layers/interaction/interaction-layer.svelte';
	import SuggestionLayer from '../layers/interaction/suggestion-layer.svelte';
	import ScatterplotView from '../layers/visualization/scatterplot-view.svelte';
	import BinnedScatterplotView from '../layers/visualization/binned-scatterplot-view.svelte';
	import Axes from '../layers/visualization/axes.svelte';
	import UiOverlay from './ui-overlay.svelte';
	import ColorLegend from './color-legend.svelte';

	export let plotWidth: number;
	export let plotHeight: number;

	let uiVisible = true;
</script>

<main

>
	{#if $activeViewMode === 'scatter'}
		<ScatterplotView width={plotWidth} height={plotHeight} />
	{:else if $activeViewMode === 'binned'}
		<BinnedScatterplotView width={plotWidth} height={plotHeight} />
	{/if}

	<Axes width={plotWidth} height={plotHeight} />
	<SuggestionLayer width={plotWidth} height={plotHeight} />
	<BrushLayer width={plotWidth} height={plotHeight} />
	<InteractionLayer width={plotWidth} height={plotHeight} />

	{#if $activeViewMode === "binned"}
		<ColorLegend
			id="color"
			left={ plotWidth - 240 }
			top={ plotHeight - 100 }
			title=""
			blockSize={ 10 }
			steps={ 10 }
			bind:colorScale={ $colorScale }
		/>
	{/if}
	<UiOverlay width={plotWidth} height={plotHeight} visible={uiVisible} />
</main>
