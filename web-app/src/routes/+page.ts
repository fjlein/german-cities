import type { PageLoad } from './$types';

export const ssr = false;

export const load = (async ({ url, parent }) => {
	const { cities }: { cities: City[] } = await parent();

	const prefix = url.searchParams.get('prefix') ?? '';
	const infix = url.searchParams.get('infix') ?? '';
	const suffix = url.searchParams.get('suffix') ?? '';
	let limit = url.searchParams.get('limit') ?? '';
	let search = url.searchParams.get('search');

	if (limit && !Number.isInteger(Number(limit))) {
		limit = '';
	}

	const filtered_cities: City[] = cities.filter((city) => {
		const name = city.name.toLowerCase();
		return (
			name.includes(infix.toLowerCase()) &&
			name.startsWith(prefix.toLowerCase()) &&
			name.endsWith(suffix.toLowerCase())
		);
	});

	return { prefix, infix, suffix, cities: filtered_cities, pro: search === 'pro' };
}) satisfies PageLoad;
