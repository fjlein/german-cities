import type { LayoutLoad } from './$types';
import c from '$lib/assets/cities.json';

export const load = (async () => {
	const cities = c as City[];
	const cities_with_coords = cities.filter((city) => city.lat && city.lon);
	const full_count = cities.length;
	const coordinate_count = cities_with_coords.length;

	return { cities: cities_with_coords, full_count, coordinate_count };
}) satisfies LayoutLoad;
