import type { LayoutLoad } from './$types';
import c from '$lib/assets/cities.json';

export const load = (async () => {
	const cities = c as City[];
	const full_count = cities.length;
	const coordinate_count = cities.filter((city) => city.lat && city.lon).length;

	return { cities, full_count, coordinate_count };
}) satisfies LayoutLoad;
