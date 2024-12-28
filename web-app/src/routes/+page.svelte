<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import Footer from '$lib/components/footer.svelte';
	import Header from '$lib/components/header.svelte';

	let { data }: { data: PageData } = $props();

	let map: L.Map;
	let mapElement: HTMLElement;

	let cities: City[] = $derived.by(() => {
		let state = $state(data.cities);
		return state;
	});

	let polyline: L.LatLngExpression[];

	let markerGroup: L.LayerGroup = L.layerGroup();

	let markers: L.Marker[] = $derived.by(() => {
		let m = [];
		for (const city of cities) {
			const marker = L.marker([city.lat, city.lon], {
				icon: L.icon({
					iconUrl: 'marker.png',
					iconSize: [30, 40],
					iconAnchor: [15, 40],
					popupAnchor: [0, -40]
				})
			});
			marker.bindPopup(city.name, { closeButton: false });
			m.push(marker);
		}
		return m;
	});

	function addMarkers() {
		map.removeLayer(markerGroup);
		markerGroup = L.layerGroup(markers.slice(0, 100));
		map.addLayer(markerGroup);
	}

	$effect(() => {
		markers;
		if (map) {
			addMarkers();
			map.setView([51, 10.5], L.Browser.mobile ? 5.5 : 6);
		}
	});
	onMount(() => {
		initMap();
		addMarkers();
	});

	function initMap() {
		map = L.map(mapElement, {
			center: [51, 10.5],
			zoomSnap: 0.5,
			zoom: L.Browser.mobile ? 5.5 : 6
		}).addLayer(
			L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
				// maxZoom: 10,
				minZoom: 5,
				attribution:
					'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
			})
		);
	}
</script>

<Header {data}></Header>
<div class="h-3"></div>
<div class="aspect-[4/5] w-full rounded-xl" bind:this={mapElement}></div>
<div class="h-1"></div>
<p class="text-muted-foreground font-mono text-xs">Only showing the biggest 100 cities.</p>
<div class="h-3"></div>
<div class="">
	<p class="text-3xl">
		{#if !data.prefix && !data.infix && !data.suffix}
			All {data.coordinate_count} cities<a href="#explainer">*</a>:
		{/if}
		{cities.map(({ name }) => name).join(', ')}
	</p>
</div>
<div class="h-3"></div>
<p id="explainer" class="text-muted-foreground font-mono text-xs">
	*that I found the coordinates for
</p>
<div class="h-24"></div>
<Footer />
