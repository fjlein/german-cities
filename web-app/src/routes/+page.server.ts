import type { PageServerLoad } from './$types';
import { turso } from '$lib/turso';

export const load = (async () => {
	const { rows } = await turso.execute('SELECT * FROM cities');

	return { rows };
}) satisfies PageServerLoad;
