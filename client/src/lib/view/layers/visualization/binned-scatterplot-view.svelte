<script lang="typescript">
	import { max, min } from 'd3-array';
	import type { HexbinBin } from 'd3-hexbin';
	import { afterUpdate, onMount } from 'svelte';

	import { hexbinning } from '$lib/state/hexbinning';
	import { visibleData } from '$lib/state/visible-data';
	import type DataItem from '$lib/types/data-item';
	import { colorScale } from '$lib/state/active-color-scale';
import ColorLegend from '$lib/view/main/color-legend.svelte';

	export let id = 'binned-scatterplot-view';
	export let width = 100;
	export let height = 100;

	$: bins = $hexbinning($visibleData);

	let updateInterval: number;
	let canvasElement: HTMLCanvasElement;

	function renderBins(ctx: CanvasRenderingContext2D, hexagonPath: Path2D) {
		clearInterval(updateInterval);
		ctx.clearRect(0, 0, width, height);
		ctx.beginPath();
		ctx.strokeStyle = 'rgba(255,255,255,1)';
		ctx.lineWidth = 2;
		bins.forEach((bin) => {
			ctx.translate(bin.x, bin.y);
			ctx.fillStyle = $colorScale(bin.length);
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

		if ($colorScale.range().length === 3) {
			$colorScale.domain([maxCount, 0, minCount]);
		} else {
			$colorScale.domain([minCount, maxCount]);
		}

		renderBins(ctx, hexagonPath);
	}

	afterUpdate(() => {
		updateInterval = setTimeout(render, 0) as unknown as number;
	});
	onMount(render);
</script>

<div id="{id}-binned-scatterplot-view" class="binned-scatterplot-view">
	<canvas id="{id}-bins-canvas" class="bins-canvas" {width} {height} bind:this={canvasElement} />

	<ColorLegend
		id="color"
		left={ width - 245 }
		top={ height - 160 }
		title=""
		blockSize={ 10 }
		steps={ 10 }
		bind:colorScale={ $colorScale }
	/>
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
