<script lang="typescript">
  export let id: string;
  export let value: number;
	export let disabled = false;
</script>

<input id="{id}-number-input" class="number-input" type="number" bind:value={ value } {disabled} />

<style>
	input.number-input {
		width: 50px;
		margin: 0 7px;
		padding: 0 5px;
		height: 18px;
		font-size: 14px;
		font-family: sans-serif;
		border: 1px solid transparent;
		border-radius: 3px;
    -moz-appearance: textfield;
		text-align: center;
		background: #333;
		color: white;
		font-weight: bold;
	}
	input.number-input:disabled {
		background: black;
		color: white;
	}
	input.number-input::-webkit-outer-spin-button,
	.number-input::-webkit-inner-spin-button {
		-webkit-appearance: none;
	}
	input.number-input:enabled:hover {
		background: #555;
	}
	input.number-input:focus {
		background: white;
		color: black;
	}
	input.number-input:focus:hover {
		background: white;
	}
</style>