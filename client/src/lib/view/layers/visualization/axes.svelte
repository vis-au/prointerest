<script lang="typescript">
	import { afterUpdate } from 'svelte';
	import { axisBottom, axisLeft } from 'd3-axis';
	import type { Selection } from 'd3-selection';
	import { select } from 'd3-selection';

	import { scaleX, scaleY } from '$lib/state/scales';
	import { currentTransform } from '$lib/state/zoom';
	import { activeViewEncodings } from '$lib/state/active-view-encodings';

	export let width: number;
	export let height: number;
	let svg: SVGElement;

	$: xAxis = axisBottom($currentTransform.rescaleX($scaleX)).tickSize(height - 20);
	$: yAxis = axisLeft($currentTransform.rescaleY($scaleY)).tickSize(width - 20);

	function styleAxes(g: Selection<SVGGElement, unknown, null, undefined>) {
		g.select('path.domain').remove();
		g.selectAll('.tick line').attr('stroke-opacity', 0.5).attr('stroke-dasharray', '2,2');
	}

	afterUpdate(() => {
		const canvas = select(svg);
		canvas.selectAll('g.axis').remove();
		canvas.append('g').attr('class', 'axis x').call(xAxis).call(styleAxes);
		canvas
			.append('g')
			.attr('class', 'axis y')
			.attr('transform', `translate(${width},0)`)
			.call(yAxis)
			.call(styleAxes);
	});
</script>

<svg bind:this={svg} id="axes" {width} {height}>
	<text class="label x" transform="translate({width / 2},{height - 2})"
		>{$activeViewEncodings.x}</text
	>
	<text class="label y" transform="translate({2},{height / 2})rotate(90)"
		>{$activeViewEncodings.y}</text
	>
</svg>

<style>
	svg#axes {
		position: absolute;
	}
	text.label {
		text-anchor: middle;
	}
</style>
