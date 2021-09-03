<script lang="typescript">
	import { max, min } from 'd3-array';
	import type { HexbinBin } from 'd3-hexbin';
	import { scaleSequential } from 'd3-scale';
	import { interpolateBuPu } from 'd3-scale-chromatic';
	import { afterUpdate, onMount } from 'svelte';

	import { hexbinning } from '$lib/state/hexbinning';
	import { visibleData } from '$lib/state/visible-data';
	import type DataItem from '$lib/types/data-item';

	export let id = 'binned-scatterplot-view';
	export let width = 100;
	export let height = 100;
	export let color = scaleSequential(interpolateBuPu);

	$: bins = $hexbinning($visibleData);

	let canvasElement: HTMLCanvasElement;

	function renderBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
		ctx.clearRect(0, 0, width, height);
		ctx.beginPath();
		ctx.strokeStyle = 'rgba(255,255,255,1)';
		ctx.lineWidth = 2;
		bins.forEach((bin) => {
			ctx.translate(bin.x, bin.y);
			ctx.fillStyle = color(bin.length);
			ctx.stroke(hexagonPath);
			ctx.fill(hexagonPath);
			ctx.translate(-bin.x, -bin.y);
		});
		ctx.closePath();
	}

	function render() {
		if (!canvasElement) {
			return;
		}

		const ctx = canvasElement.getContext('2d');
		const hexagonPath = new Path2D($hexbinning.hexagon());

		const minCount = min(bins, (d: HexbinBin<DataItem>) => d.length) || 0;
		const maxCount = max(bins, (d: HexbinBin<DataItem>) => d.length) || 1;

		if (color.range().length === 3) {
			color.domain([maxCount, 0, minCount]);
		} else {
			color.domain([minCount, maxCount]);
		}

		renderBins(ctx, hexagonPath);
	}

	afterUpdate(() => {
		setTimeout(render, 0);
	});
	onMount(render);
</script>

<div id="{id}-binned-scatterplot-view" class="binned-scatterplot-view">
	<canvas id="{id}-bins-canvas" class="bins-canvas" {width} {height} bind:this={canvasElement} />
</div>

<style>
	div.binned-scatterplot-view {
		position: relative;
	}
	div.binned-scatterplot-view canvas.bins-canvas {
		position: absolute;
		background: #efefef;
	}
</style>
