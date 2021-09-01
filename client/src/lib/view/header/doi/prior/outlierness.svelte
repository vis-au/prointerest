<script>
	import { selectedOutlierMeasure } from '$lib/state/selected-outlier-measure';
	import { outliernessMeasures } from '$lib/types/outlier-measures';
	import Alternatives from '$lib/widgets/alternatives.svelte';
	import BigNumber from '$lib/widgets/big-number.svelte';
	import DoiConfig from '$lib/widgets/doi-config.svelte';
</script>

<DoiConfig
	title="Set outlier measure"
	message="You can choose between three different outlierness metrics that are used to determine whether a data item is an outlier or not."
	width={400}
>
	<Alternatives
		name="outlierness-measure"
		alternatives={outliernessMeasures}
		bind:activeAlternative={$selectedOutlierMeasure}
	/>

	<p class="explanation">
		Info:
		{#if $selectedOutlierMeasure === 'tukey'}
			The "tukey" measure captures outlierness by determining, if the item falls outside the Tukey
			ranges across <BigNumber>75%</BigNumber> of the data.
		{:else if $selectedOutlierMeasure === 'scagnostic'}
			The "scagnostics" measure captures outlierness by determining if the item returns an
			outlierness scagnostic value of greater than <BigNumber>.95</BigNumber>.
		{:else if $selectedOutlierMeasure === 'clustering'}
			The "clustering" measure captures outlierness by determining, if the item is assigned its own
			cluster when applying DBSCAN to the data.
		{/if}
	</p>
</DoiConfig>

<style>
	p.explanation {
		color: #999;
	}
</style>
