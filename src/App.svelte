<script>
	import {onMount} from "svelte";
	let base_url = "https://143d-2001-620-618-5a0-2-80b3-0-5fa.eu.ngrok.io"
	let out;
	onMount(()=>{
	fetch(base_url + "/sustainable_models" + "?uid=" + "tsf-460-wpa-6-019.epfl.ch0").then(
		(data) => data.json()

	).then((data) => {
		out = data;
		console.log(out);
	});});
</script>

<main>
	{#if out}
		<div class="box">
			Data Metrics:
			<div class="mini-box">
				<h1>{"Carbon carbon_comparison"}</h1>
				<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["carbon_comparison"]}</p>
			</div>
		</div>
	{/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		margin: 0 auto;
		width: 50%;
	}
	.box {
		border: 1px solid #ccc;
		display: flex;
		flex-direction: row;
	}
	.mini-box {
		border: 1px solid #ccc;
		display: flex;
		flex-direction: column;
		height: 100%;
	}


</style>