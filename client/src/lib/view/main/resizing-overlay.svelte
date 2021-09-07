<script lang="typescript">
	import { isResizing } from '$lib/state/is-resizing';
	import Column from '$lib/widgets/column.svelte';

	export let x: number;
	export let y: number;

	let width = 200;
	let innerWidth = -1;

	const margin = 20;

	$: leftLabel = $isResizing?.leftId;
	$: rightLabel = $isResizing?.rightId;
	$: leftValue = Math.round($isResizing?.leftValue * 10000) / 100;
	$: rightValue = Math.round($isResizing?.rightValue * 10000) / 100;

	$: left = $isResizing
		? `left:${Math.min(Math.max(x - width / 2, 0), innerWidth - width - margin)}px`
		: 'left: 0';
	$: top = $isResizing ? `top:${y + margin}px` : 'top: 0';
</script>

<div
	class="resizing-overlay {$isResizing === null ? 'hidden' : ''}"
	style="{left};{top};min-width:{width}px;"
	bind:clientWidth={width}
>
	<Column>
		<div class="label">{leftLabel}</div>
		<div class="value">{leftValue}%</div>
	</Column>
	<div class="center">{'⬌'}</div>
	<Column>
		<div class="label">{rightLabel}</div>
		<div class="value">{rightValue}%</div>
	</Column>
</div>

<svelte:window bind:innerWidth />

<style>
	div.resizing-overlay {
		position: absolute;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		background: white;
		padding: 15px 20px;
		border: 1px solid #ccc;
		border-radius: 3px;
	}
	div.resizing-overlay.hidden {
		display: none;
	}
	div.center {
		padding: 0 20px;
	}
	div.label {
		text-align: center;
		font-weight: bold;
	}
	div.value {
		text-align: center;
	}
</style>
