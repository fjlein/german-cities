import { turso } from '$lib/turso';
import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
	const prefix = url.searchParams.get('prefix');
	const infix = url.searchParams.get('infix');
	const suffix = url.searchParams.get('suffix');
	let limit = url.searchParams.get('limit');

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

	if (!limit) {
		limit = '10000';
	}

	query += ` LIMIT ${limit}`;

	const result = await turso.batch([
		{
			sql: query,
			args: params
		},
		'SELECT COUNT(name) FROM cities'
	]);

	const city_rows = result[0].rows;
	const count_rows = result[1].rows;

	console.log(count_rows);

	const cities: City[] = city_rows as unknown as City[];

	return json(cities);
};
