import { turso } from '$lib/turso';
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
	const prefix = url.searchParams.get('p');
	const infix = url.searchParams.get('i');
	const suffix = url.searchParams.get('s');

	const conditions: string[] = [];
	const params: string[] = [];

	if (prefix) {
		conditions.push('name LIKE ?');
		params.push(`${prefix}%`);
	}

	if (infix) {
		conditions.push('name LIKE ?');
		params.push(`%${infix}%`);
	}

	if (suffix) {
		conditions.push('name LIKE ?');
		params.push(`%${suffix}`);
	}

	let query = `
    SELECT * 
    FROM cities
    WHERE lat IS NOT NULL 
    AND lon IS NOT NULL
	`;

	if (conditions.length > 0) {
		query += ` AND (${conditions.join(' AND ')})`;
	}

	const { rows } = await turso.execute({
		sql: query,
		args: params
	});

	const cities: City[] = rows as unknown as City[];

	return json(cities);
};
