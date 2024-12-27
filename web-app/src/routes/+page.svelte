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
			const marker = L.marker([city.lat, city.lon]);
			marker.bindPopup(city.name);
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
			L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
				// maxZoom: 10,
				minZoom: 5,
				attribution:
					'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
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

<Header {data}></Header>
<div class="h-3"></div>

<div class="aspect-[4/5] w-full rounded-xl" bind:this={mapElement}></div>

<div class="h-3"></div>
<div class="">
	<p class="text-3xl">
		{cities.map(({ name }) => name).join(', ')}
	</p>
</div>
<div class="h-24"></div>
<Footer />
