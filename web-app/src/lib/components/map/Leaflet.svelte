<script lang="ts">
	import L from 'leaflet';
	import { onDestroy, onMount, setContext, type Snippet } from 'svelte';

	let { children }: { children?: Snippet } = $props();

	let map: L.Map | undefined;
	let mapElement: HTMLDivElement;

	onMount(() => {
		let mapOptions: L.MapOptions = {
			center: [51.336, 10.357],
			zoom: 6.2
		};

		map = L.map(mapElement, mapOptions);

		L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		}).addTo(map);
	});

	onDestroy(() => {
		map?.remove();
		map = undefined;
	});

	setContext('map', {
		getMap: () => map
	});
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
		integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
		crossorigin=""
	/>
</svelte:head>

<div class="h-[800px] w-[600px] border" bind:this={mapElement}>
	{@render children?.()}
</div>
