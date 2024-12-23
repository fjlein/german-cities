import type { PageLoad } from './$types';

export const ssr = false;

export const load = (async ({ url, fetch }) => {
	const p = url.searchParams.get('p') ?? '';
	const i = url.searchParams.get('i') ?? '';
	const s = url.searchParams.get('s') ?? '';

	console.log(`/api/cities?p=${p}&i=${i}&s=${s}`);

	const res = await fetch(`/api/cities?p=${p}&i=${i}&s=${s}`);
	const cities: City[] = await res.json();

	return { p, i, s, cities };
}) satisfies PageLoad;
