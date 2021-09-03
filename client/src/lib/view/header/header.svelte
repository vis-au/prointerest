<script lang="typescript">
	import Row from '$lib/widgets/row.svelte';
	import PosteriorWeights from './posterior-weights.svelte';
	import PriorWeights from './prior-weights.svelte';

	export let height;
</script>

<header>
	<div class="title">
		<img src="static/logo.svg" alt="the ProInterest logo" height={height} />
	</div>
	<Row id="doi-configuration" style="{height}px">
		<PriorWeights />
		<PosteriorWeights />
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
