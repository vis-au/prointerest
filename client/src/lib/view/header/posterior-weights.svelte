<script lang="typescript">
	import { posteriorWeights } from '$lib/state/active-doi-weights';
	import { selectedDoiWeight } from '$lib/state/selected-doi-weight';
	import { sendWeights } from '$lib/util/requests';
	import Row from '$lib/widgets/row.svelte';
	import WeightedValues from '$lib/widgets/weighted-values.svelte';
</script>

<Row>
	<h2>Posterior</h2>
	<WeightedValues
		group="doi-weights"
		totalSize={350}
		bind:valueWeights={$posteriorWeights}
		bind:activeWeight={$selectedDoiWeight}
		on:end={() => sendWeights('posterior', $posteriorWeights)}
	/>
</Row>

<style>
	h2 {
		margin: 0;
		font-size: 12pt;
		margin-right: 10px;
		margin-left: 30px;
	}
</style>
