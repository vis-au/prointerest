<script lang="typescript">
	import { activeDoiValues } from '$lib/state/latest-doi-values';
	import { quadtree } from '$lib/state/quadtree';
	import { getDoiValues } from '$lib/util/requests';
	import Row from '$lib/widgets/row.svelte';

	import ControlButton from '../main/control-button.svelte';
	import PosteriorWeights from './posterior-weights.svelte';
	import PriorWeights from './prior-weights.svelte';

	export let height: number;

	async function evaluateInterest() {
		const doiValues = await getDoiValues($quadtree.data());
		const map = new Map<number, number>();
		doiValues.forEach((pair) => map.set(pair[0], pair[1]));
		$activeDoiValues = map;
	}
</script>

<header>
	<div class="title">
		<img src="static/logo.svg" alt="the ProInterest logo" {height} />
	</div>
	<Row id="doi-configuration" style="{height}px">
		<PriorWeights />
		<PosteriorWeights />
		<ControlButton
			style="background:limegreen;margin:0 10px;padding:5px 10px"
			on:click={evaluateInterest}
		>
			Update Interest
		</ControlButton>
	</Row>
</header>

<style>
	header {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		background: white;
		border-bottom: 1px solid #ddd;
	}

	header div.title {
		display: flex;
		flex-direction: row;
		align-items: center;
	}
</style>
