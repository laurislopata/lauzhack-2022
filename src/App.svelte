<script>
	import {onMount} from "svelte";
	let base_url = "https://b77b-2001-620-618-5a0-2-80b3-0-5fa.eu.ngrok.io";
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
		<div class="header"> Clean Code </div>
		<div class= "box"> Parameters: 
			<div class= "mini-box"> 
				<p> Input size:  </p>
				<input value={name}>
			</div>

			<div class= "mini-box"> 
				<p> Estimation api calls: </p>
				<input value={name}>
			</div> 	
		</div>

		<div class= "header1">
			<p> Data Metrics: </p>
		</div>
		<div class="box">
			<div class="mini-box">
				<h1>{"Monetary: "}</h1>
				<div class= "cost">
					<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["monetary_cost"] + " CHF"}</p>
				</div>
			</div>
			
			<div class="mini-box">
				<h1>{"Electricity: "}</h1>
				<div class= "cost">
					<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["electricity_cost"] + "kWh"}</p>
				</div>
				<div class= "comparison">
					<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["electricity_comparison"]}</p>
				</div>
			</div>

			<div class="mini-box">
				<h1>{"Carbon Estimate: "}</h1>
				<div class= "cost">
					<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["carbon_cost"] + "gC02"}</p>
				</div>
				<div class= "comparison">
					<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["carbon_comparison"] }</p>
				</div>
			</div>
		</div>

		Action Points:
		<div class="box">
			<div class="mini-box">
				<h1>{"Load balance: "}</h1>
				<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["hardware_recommendation"]}</p>
			</div>
			<div class="mini-box">
				<h1>{"Scheduler: "}</h1>
				<p>{out["tsf-460-wpa-6-019.epfl.ch0"]["server_region_recommendation"]}</p>
			</div>
		</div>

	{/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		margin: 0 auto;
		width: 100%;

	}
	.header {
		font-size: 4em;
	}


	.box {
		border: 0px solid #ccc;
		display: flex;
		flex-direction: row;
		height: 100%;
		width: 100%;
	}
	.mini-box {
		border: 0px solid #ccc;
		display: flex;
		flex-direction: column;
		text-align: center;
		margin: auto;
		width: 100%;
	}

	.header1{
		font-size: 2em;
		display: flex;
		flex-direction: row;
		text-align: left;
	}

	.header2{
		font-size: 2em;
		display: flex;
		flex-direction: row;
	}

	.cost{
		border: 0px solid #ccc;
		display: flex;
		flex-direction: row;
		text-align: center;
		margin: auto;
	}

	.comparison{
		border: 0px solid #ccc;
		display: flex;
		flex-direction: row;
		text-align: center;
		margin: auto;
		width: 100%;
	}

</style>