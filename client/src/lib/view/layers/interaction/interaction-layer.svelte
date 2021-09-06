<script lang="typescript">
	import { afterUpdate, onMount } from 'svelte';
	import { brush } from 'd3-brush';
	import type { D3BrushEvent } from 'd3-brush';
	import { select } from 'd3-selection';
	import type { Selection } from 'd3-selection';
	import { zoom, zoomTransform } from 'd3-zoom';
	import type { D3ZoomEvent } from 'd3-zoom';

	import { hoveredPosition } from '$lib/state/hovered-position';
	import { selectedBins } from '$lib/state/selected-bins';
	import { currentTransform, isZooming } from '$lib/state/zoom';
	import { hexbinning } from '$lib/state/hexbinning';
	import { activeBrush } from '$lib/state/active-brush';
	import { activeInteractionMode } from '$lib/state/active-interaction-mode';
	import InteractionFactory from '$lib/interaction/doi-interaction-factory';
	import type DataItem from '$lib/types/data-item';
	import { getDummyDataItem } from '$lib/util/dummy-data-item';
	import { quadtree } from '$lib/state/quadtree';
	import { getPointsInRect } from '$lib/util/find-in-quadtree';
	import type { DoiInteraction } from '$lib/interaction/doi-interaction';
	import { getLatestTimestamp, registerNewInteraction } from '$lib/state/interesting-items';

	export let id = 'view-interaction-layer';
	export let width: number;
	export let height: number;
	export let color = 'rgba(255,255,255,1)';
	export let lineWidth = 4;

	let selectionCanvas: HTMLCanvasElement;
	let zoomCanvasElement: HTMLCanvasElement;
	let brushCanvasElement: SVGElement;

	const interactionFactory = new InteractionFactory(width, height, $quadtree);
	interactionFactory.getItemsInRegion = getPointsInRect;
	interactionFactory.getTimestamp = getLatestTimestamp;

	const zoomBehavior = zoom()
		.scaleExtent([0.75, 10])
		.on('start', () => ($isZooming = true))
		.on('zoom', onZoom)
		.on('end', onZoomEnd);

	const brushBehavior = brush().on('end', onBrushEnd);

	function onInteraction(interaction: DoiInteraction) {
		registerNewInteraction(interaction);
	}

	function onZoom(event: D3ZoomEvent<Element, void>) {
		if (event.sourceEvent === null) {
			return;
		}

		$currentTransform = event.transform;
	}

	function onZoomEnd() {
		$isZooming = false;
		const interaction = interactionFactory.createZoomInteraction($currentTransform);
		onInteraction(interaction);
	}

	function onHover(event) {
		const rect = event.target.getBoundingClientRect();
		const x = $currentTransform.invertX(event.clientX - rect.left);
		const y = $currentTransform.invertY(event.clientY - rect.top);

		hoveredPosition.set([x, y]);
	}

	function onClick(event) {
		const rect = event.target.getBoundingClientRect();
		const x = $currentTransform.invertX(event.clientX - rect.left);
		const y = $currentTransform.invertY(event.clientY - rect.top);

		const dummyItem = getDummyDataItem();
		dummyItem.position = { x, y };
		const clickedBin = $hexbinning([dummyItem])[0];
		const selectedBin = $selectedBins.find(
			(bin) => bin.x === clickedBin.x && bin.y === clickedBin.y
		);
		const selectedIndex = $selectedBins.indexOf(selectedBin);

		selectedBins.update((currentlySelectedBins) => {
			if (selectedIndex > 0) {
				currentlySelectedBins.splice(selectedIndex, 1);
				return currentlySelectedBins;
			} else {
				return (currentlySelectedBins = currentlySelectedBins.concat([clickedBin]));
			}
		});

		const interaction = interactionFactory.createSelectInteraction(x, y);
		onInteraction(interaction);
	}

	function onBrushEnd(event: D3BrushEvent<DataItem>) {
		const selection = event.selection;

		if (selection === null || selection === undefined) {
			$activeBrush = [
				[null, null],
				[null, null]
			];
			return;
		}

		const [[x0, y0], [x1, y1]] = selection as [[number, number], [number, number]];
		const _x0 = $currentTransform.invertX(x0);
		const _y0 = $currentTransform.invertY(y0);
		const _x1 = $currentTransform.invertX(x1);
		const _y1 = $currentTransform.invertY(y1);
		$activeBrush = [
			[_x0, _y0],
			[_x1, _y1]
		];

		// the brush is drawn by the brush-layer component to make the brushed region persist zoom+pan
		// we can therefore hide it here
		select(brushCanvasElement).selectAll('rect.selection,rect.handle').style('display', 'none');

		const interaction = interactionFactory.createBrushInteraction(_x0, _y0, _x1, _y1);
		onInteraction(interaction);
	}

	function renderHoveredBin(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
		const dummyItem = getDummyDataItem();
		dummyItem.position.x = $hoveredPosition[0];
		dummyItem.position.y = $hoveredPosition[1];
		const hoveredBin = $hexbinning([dummyItem])[0];

		if (!hoveredBin) {
			return;
		}

		ctx.beginPath();
		ctx.translate(hoveredBin.x, hoveredBin.y);
		ctx.strokeStyle = color;
		ctx.fillStyle = 'rgba(0, 0, 0, 0.0)';
		ctx.lineWidth = lineWidth;
		ctx.stroke(hexagonPath);
		ctx.fill(hexagonPath);
		ctx.translate(-hoveredBin.x, -hoveredBin.y);
		ctx.closePath();
	}

	function renderSelectedBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
		ctx.beginPath();
		ctx.strokeStyle = color;
		ctx.fillStyle = 'rgba(0, 0, 0, 0.0)';
		ctx.lineWidth = lineWidth;
		$selectedBins.forEach((bin) => {
			ctx.translate(bin.x, bin.y);
			ctx.stroke(hexagonPath);
			ctx.fill(hexagonPath);
			ctx.translate(-bin.x, -bin.y);
		});
		ctx.closePath();
	}

	function render() {
		if (!selectionCanvas) {
			return;
		}

		const hexagonPath = new Path2D($hexbinning.hexagon());
		const ctx = selectionCanvas.getContext('2d');
		ctx.clearRect(0, 0, width, height);

		renderHoveredBin(ctx, hexagonPath);
		renderSelectedBins(ctx, hexagonPath);
	}

	onMount(() => {
		// use a timeout to ensure that the brush canvas has the right size when calling the brush
		// behavior
		setTimeout(() => {
			const brushSvg = select(brushCanvasElement);
			brushSvg.call(brushBehavior);
			const zoomCanvas = select(zoomCanvasElement);
			zoomCanvas.call(zoomBehavior);
		}, 10);
	});

	afterUpdate(() => {
		const canvas = select(zoomCanvasElement) as Selection<Element, unknown, null, null>;
		const myZoom = zoomTransform(zoomCanvasElement);

		// check if the zoom transform has changed
		if (JSON.stringify(myZoom) !== JSON.stringify($currentTransform)) {
			zoomBehavior.transform(canvas, $currentTransform);
		}

		render();
	});
</script>

<div class="interaction-canvas-container {$isZooming ? "zooming" : ""}">
	<canvas
		id="{id}-selection-canvas"
		class="selection interaction-canvas"
		{width}
		{height}
		bind:this={selectionCanvas}
	/>
	<canvas
		id="{id}-zoom-canvas"
		class="zoom interaction-canvas {$activeInteractionMode !== 'zoom' ? 'hidden' : ''}"
		{width}
		{height}
		on:mousemove={onHover}
		on:click={onClick}
		bind:this={zoomCanvasElement}
	/>
	<svg
		id="{id}-brush-canvas"
		class="brush interaction-canvas {$activeInteractionMode !== 'brush' ? 'hidden' : ''}"
		{width}
		{height}
		on:mousemove={onHover}
		on:click={onClick}
		bind:this={brushCanvasElement}
	/>
</div>

<style>
	div.interaction-canvas-container {
		position: relative;
	}
	div.interaction-canvas-container.zooming {
		cursor: all-scroll;
	}
	canvas.interaction-canvas,
	svg.interaction-canvas {
		position: absolute;
	}
	canvas.interaction-canvas.hidden,
	svg.interaction-canvas.hidden {
		display: none;
	}
</style>
