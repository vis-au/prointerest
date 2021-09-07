<script lang="typescript">
	import { dimensions, totalSize } from '$lib/state/processed-data';
	import Header from '$lib/view/header/header.svelte';
	import MainView from '$lib/view/main/main-view.svelte';
	import { onMount } from 'svelte';
	import { hexbinning } from '$lib/state/hexbinning';
	import { currentTransform } from '$lib/state/zoom';
	import ActiveDoiPanel from '$lib/view/header/doi/active-doi-panel.svelte';
	import { quadtree } from '$lib/state/quadtree';
	import { scaleX, scaleY } from '$lib/state/scales';
	import { isResizing } from '$lib/state/is-resizing';
	import ResizingOverlay from '$lib/view/main/resizing-overlay.svelte';
	import { getDimensionNames, getTotalDatasize } from '$lib/util/requests';
	import ProgressionControls from '$lib/view/main/progression-controls.svelte';
	import { activeViewEncodings } from '$lib/state/active-view-encodings';
	import { viewPort } from '$lib/state/visible-data';

	let innerWidth = 0;
	let innerHeight = 0;
	let mousePosition = [-1, -1];

	const headerHeight = 35;
	const margin = {
		horizontal: 2,
		vertical: headerHeight + 2
	};

	$: plotWidth = innerWidth - margin.horizontal;
	$: plotHeight = innerHeight - margin.vertical;
	$: $viewPort.maxX = innerWidth;
	$: $viewPort.maxY = innerHeight;

	$: $scaleX?.range([0, plotWidth]);
	$: $scaleY?.range([0, plotHeight]);

	onMount(() => {
		setTimeout(async () => {
			// triggers the rendering of the binned scatterplot
			$hexbinning = $hexbinning;
			// triggers the rendering of the scatterplot
			$currentTransform = $currentTransform;

			$quadtree = $quadtree.extent([
				[0, 0],
				[innerWidth, innerHeight]
			]);

			$dimensions = await getDimensionNames();
			$activeViewEncodings.x = 'trip_distance';
			$activeViewEncodings.y = 'total_amount';

			$totalSize = await getTotalDatasize();
		}, 0);
	});
</script>

<div id="pro-interest">
	<Header height={headerHeight} />
	<MainView {plotWidth} {plotHeight} />
	<ActiveDoiPanel />
	<ResizingOverlay x={mousePosition[0]} y={$isResizing?.startY} />
	<ProgressionControls x={plotWidth - 240} y={plotHeight - 20} />
</div>

<svelte:window bind:innerWidth bind:innerHeight />

<svelte:body on:mousemove={(e) => (mousePosition = [e.clientX, e.clientY])} />

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
