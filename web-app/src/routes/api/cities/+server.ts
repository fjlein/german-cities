import { turso } from '$lib/turso';
import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
	console.log('API called');

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
		'SELECT COUNT(name) FROM cities',
		'SELECT COUNT(name) FROM cities WHERE lat IS NOT NULL AND lon IS NOT NULL'
	]);

	const city_rows = result[0].rows;
	const full_count_rows = result[1].rows;
	const coordinate_count_rows = result[2].rows;

	const full_count: number = full_count_rows[0]['COUNT(name)'] as unknown as number;
	const coordinate_count: number = coordinate_count_rows[0]['COUNT(name)'] as unknown as number;

	const cities: City[] = city_rows as unknown as City[];

	return json({ cities, full_count, coordinate_count });
};
