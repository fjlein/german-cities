<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';

	let { data }: { data: PageData } = $props();

	let map: L.Map;
	let mapElement: HTMLElement;

	let cities: City[] = data.cities;
	let polyline: L.LatLngExpression[];

	onMount(() => {
		map = L.map(mapElement, {
			center: [51.558, 10.141],
			zoom: 6.2
		}).addLayer(
			L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
				// maxZoom: 10,
				minZoom: 5,
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
			})
		);

		cities.forEach((city) => {
			const marker = L.marker([city.lat, city.lon]);
			marker.bindPopup(city.name);
			marker.addTo(map);
		});

		// const points: salesman.Point[] = cities.map((city) => {
		// 	return new salesman.Point(city.lat, city.lon);
		// });

		// const solution: number[] = salesman.solve(points, 0.999999, co);
		// const ordered_points: salesman.Point[] = solution.map((i) => points[i]);

		// const paths = ordered_points.map((point, index) => {
		// 	const nextPoint = ordered_points[(index + 1) % ordered_points.length]; // Wrap around to the first point
		// 	return {
		// 		from: { x: point.x, y: point.y },
		// 		to: { x: nextPoint.x, y: nextPoint.y }
		// 	};
		// });

		// console.log(paths);

		// paths.forEach((path) => {
		// 	console.log(path);
		// 	L.polyline([
		// 		[path.from.x, path.from.y],
		// 		[path.to.x, path.to.y]
		// 	]).addTo(map);
		// });
	});
</script>

<div class="h-[600px] w-[500px]" bind:this={mapElement}></div>
