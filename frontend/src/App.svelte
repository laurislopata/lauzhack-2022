<script>
	import { onMount } from "svelte";
	import axios from "axios";
	// import { ChatGPTAPI } from './chatgpt-api';
	onMount(() => {
		async function fetchData() {
			reload();
		}

		const interval = setInterval(fetchData, 3000);
		fetchData();

		return () => clearInterval(interval);
	});
	let name;
	let url = "http://localhost:5000";
	let containers;
	async function reload() {
		axios
			.get(url + "/containers")
			.then((res) => res.data)
			.then((data) => {
				console.log(data);
				containers = data;
			});
	}

	function addContainer() {
		axios.get(url + "/start/" + name).then(() => {
			reload();
			name = "";
		});
	}

	let inputCode = "";
</script>

<main>
	Welcome to Docker Reactive Manager.
	<!-- <div>
		Start an image : <input bind:value={name} />
		<button on:click={addContainer}>Add</button>
		<ul style="width: 100%">
			{#if containers}
				{#each containers as item}
					<li class="item">
						<div class="item">
							<div class="id">
								<div>Name: {item.name}</div>
								<div>Id: {item.id.substring(0, 10)}</div>
								<div>Status: {item.status}</div>
								{#if item.status == "running"}
									<div>
										<button
											on:click={() => {
												axios
													.get(
														url + "/stop/" + item.id
													)
													.then(() => reload());
											}}>Pause</button
										>
										<button
											on:click={() => {
												axios
													.get(
														url + "/kill/" + item.id
													)
													.then(() => reload());
											}}>Kill</button
										>
									</div>
								{:else}
									<button
										on:click={() => {
											axios
												.get(url + "/start/" + item.id)
												.then(() => reload());
										}}>Start</button
									>
								{/if}
							</div>

							<div class="id">
								<div>
									cpu usage: {(
										item.stats.cpu_stats.cpu_usage
											.total_usage /
										item.stats.cpu_stats.system_cpu_usage
									).toFixed(0)} %
								</div>
								<div>
									memory usage: {(
										item.stats.memory_stats.usage /
										1024 /
										1024
									).toFixed(0)} / {(
										item.stats.memory_stats.limit /
										1024 /
										1024
									).toFixed(0)} KiB
								</div>
								<div>
									network usage: {item.stats.networks.eth0
										.rx_bytes}
								</div>
								<div>
									log: {item.logs}
								</div>
							</div>
						</div>
					</li>
					<hr />
				{/each}
			{/if}
		</ul>
	</div> -->

	<div>
		Input your code to predict its resource usage
		<input bind:value={inputCode} />
		<button on:click={() => axios.get(url + '/chat?q=' + 'How much memory in bytes will this code allocate? \n' + inputCode)}> Predict </button>
	</div>
</main>

<style>
	main {
		text-align: center;
	}

	.id {
		display: flex;
		flex-direction: column;
	}
	.item {
		display: flex;
		flex-direction: row;
		width: 100%;
		justify-content: space-evenly;
	}
</style>
