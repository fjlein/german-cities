import type { LayoutLoad } from './$types';

export const load = (async () => {
	const res = await fetch(`/api/cities`);
	const {
		cities,
		full_count,
		coordinate_count
	}: { cities: City[]; full_count: number; coordinate_count: number } = await res.json();

	return { cities, full_count, coordinate_count };
}) satisfies LayoutLoad;
