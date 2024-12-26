<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import salesman from 'salesman.js';
	import Footer from '$lib/components/footer.svelte';
	import Search from '$lib/components/search.svelte';
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
			const marker = L.marker([city.lat, city.lon]);
			marker.bindPopup(city.name);
			m.push(marker);
		}
		return m;
	});

	function addMarkers() {
		console.log('markers added');
		map.removeLayer(markerGroup);
		markerGroup = L.layerGroup(markers.slice(0, 100));
		map.addLayer(markerGroup);
	}

	$effect(() => {
		markers;
		if (map) {
			addMarkers();
		}
	});

	onMount(() => {
		initMap();
		addMarkers();
	});

	function initMap() {
		map = L.map(mapElement, {
			center: [51.558, 10.141],
			zoom: 6.2,
			dragging: !L.Browser.mobile
		}).addLayer(
			L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
				// maxZoom: 10,
				minZoom: 5,
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
			})
		);
	}

	// async function calculateAndAddPolyline() {
	// 	await new Promise((resolve) => setTimeout(resolve, 1000));

	// 	const points: salesman.Point[] = cities.map((city) => {
	// 		return new salesman.Point(city.lat, city.lon);
	// 	});

	// 	const solution: number[] = await new Promise<number[]>((resolve) =>
	// 		setTimeout(() => resolve(salesman.solve(points, 0.999)), 0)
	// 	);

	// 	polyline = solution.map((i) => [points[i].x, points[i].y]);

	// 	L.polyline(polyline).addTo(map);
	// }
</script>

<!-- {JSON.stringify(cities)} -->

<Search />
<div class="h-6"></div>
<Header {data}></Header>
<div class="h-6"></div>
<div class="h-[650px] w-full" bind:this={mapElement}></div>
<div class="h-6"></div>
<div class="flex flex-wrap gap-2">
	{#each cities as city}
		<div class="rounded-md bg-blue-100 px-2 py-1 text-2xl font-medium">{city.name}</div>
	{/each}
</div>
<div class="h-24"></div>
<Footer />
