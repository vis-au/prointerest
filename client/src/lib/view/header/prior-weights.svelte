<script lang="typescript">
	import { priorWeights } from '$lib/state/active-doi-weights';
	import { selectedDoiWeight } from '$lib/state/selected-doi-weight';
	import Row from '$lib/widgets/row.svelte';
	import WeightedValues from '$lib/widgets/weighted-values.svelte';
</script>

<Row>
	<h2>Prior</h2>
	<WeightedValues
		group="doi-weights"
		totalSize={400}
		bind:valueWeights={$priorWeights}
		bind:activeWeight={$selectedDoiWeight}
	/>
</Row>

<style>
	h2 {
		margin: 0;
		font-size: 12pt;
		margin-right: 10px;
	}
</style>
