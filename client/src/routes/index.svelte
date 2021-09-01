<script lang="typescript">
	import { range } from 'd3-array';

	import { dimensions, processedData } from '$lib/state/processed-data';
	import Header from '$lib/view/header/header.svelte';
	import MainView from '$lib/view/main/main-view.svelte';
	import { onMount } from 'svelte';
	import { hexbinning } from '$lib/state/hexbinning';
	import { currentTransform } from '$lib/state/zoom';
	import ActiveDoiPanel from '$lib/view/header/doi/active-doi-panel.svelte';
	import { quadtree } from '$lib/state/quadtree';
	import { scaleX, scaleY } from '$lib/state/scales';

	const data = range(0, 10000).map(() => [Math.random(), Math.random(), Math.random()] as number[]);

	let innerWidth: number;
	let innerHeight: number;

	$processedData = data;
	$dimensions = ['dimension a', 'dimension b', 'dimension c'];

	const margin = {
		horizontal: 2,
		vertical: 35
	};

	$: plotWidth = innerWidth - margin.horizontal;
	$: plotHeight = innerHeight - margin.vertical;
	$: $scaleX.range([0, plotWidth]);
	$: $scaleY.range([0, plotHeight]);

	onMount(() => {
		setTimeout(() => {
			// triggers the rendering of the binned scatterplot
			$hexbinning = $hexbinning;
			// triggers the rendering of the scatterplot
			$currentTransform = $currentTransform;

			$quadtree = $quadtree.extent([
				[0, 0],
				[innerWidth, innerHeight]
			]);
		}, 0);
	});
</script>

<div id="pro-interest">
	<Header />
	<MainView {plotWidth} {plotHeight} />
	<ActiveDoiPanel />
</div>

<svelte:window bind:innerWidth bind:innerHeight />

<style>
	:global(body) {
		margin: 0;
		padding: 0;
	}
	:global(body *) {
		font-family: Roboto;
		box-sizing: border-box;
	}
</style>
