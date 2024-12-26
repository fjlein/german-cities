import type { PageLoad } from './$types';

export const ssr = false;

export const load = (async ({ url, fetch }) => {
	const prefix = url.searchParams.get('prefix') ?? '';
	const infix = url.searchParams.get('infix') ?? '';
	const suffix = url.searchParams.get('suffix') ?? '';
	let limit = url.searchParams.get('limit') ?? '';

	if (limit && !Number.isInteger(Number(limit))) {
		limit = '';
	}

	const res = await fetch(
		`/api/cities?prefix=${prefix}&infix=${infix}&suffix=${suffix}&limit=${limit}`
	);
	const cities: City[] = await res.json();

	console.log('Jo' + cities.length + url);

	return { prefix, infix, suffix, cities };
}) satisfies PageLoad;
