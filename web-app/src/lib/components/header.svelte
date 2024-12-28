<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import Button from './ui/button/button.svelte';
	import { Input } from './ui/input';
	import finger from '$lib/assets/finger.png';
	import happy from '$lib/assets/happy.png';
	import sad from '$lib/assets/sad.png';

	let {
		data
	}: {
		data: {
			infix: string;
			prefix: string;
			suffix: string;
			cities: City[];
			pro: boolean;
			full_count: number;
			coordinate_count: number;
		};
	} = $props();

	let prefix = $state(page.data.prefix);
	let infix = $state(page.data.infix);
	let suffix = $state(page.data.suffix);

	$effect(() => {
		prefix = data.prefix;
		infix = data.infix;
		suffix = data.suffix;
	});

	let search: boolean = $derived(data.prefix === '' && data.infix === '' && data.suffix === '');

	function new_search() {
		if (!prefix && !infix && !suffix) return;
		let query = page.url.searchParams;
		query.delete('search');
		if (prefix) {
			query.set('prefix', prefix.trim().toLowerCase());
		}
		if (infix) {
			query.set('infix', infix.trim().toLowerCase());
		}
		if (suffix) {
			query.set('suffix', suffix.trim().toLowerCase());
		}
		goto(`${page.url.origin}?${query.toString()}`);
	}
</script>

<svelte:head>
	<title>All German Cities</title>
	<meta property="og:title" content="Check out this search!" />
	<meta property="og:type" content="website" />
	<meta
		property="og:description"
		content="Only {data.cities.length} out of {data.coordinate_count} cities are left!"
	/>
</svelte:head>

{#snippet simple_search()}
	<a href="/" class="text-3xl underline underline-offset-2">simple</a>
{/snippet}
{#snippet pro_search()}
	<a href="/?search=pro" class="text-3xl underline underline-offset-2">pro</a>
{/snippet}

<div class="flex flex-wrap gap-2 text-3xl">
	{#if search}
		<form
			class="flex flex-wrap gap-2"
			onsubmit={(event) => {
				event.preventDefault();
				new_search();
			}}
		>
			{#if !data.pro}
				<img src={finger} class="h-9" alt="finger pointing right" />
			{/if}

			{#if data.pro}
				<img src={finger} class="h-9" alt="finger pointing right" />
				<p class="text-3xl">prefix</p>
				<Input bind:value={prefix} type="text" class="w-36" />
			{/if}
			{#if data.pro}
				<img src={finger} class="h-9" alt="finger pointing right" />
				<p class="text-3xl">infix</p>
			{/if}
			<Input bind:value={infix} type="text" class="w-36" />
			{#if data.pro}
				<img src={finger} class="h-9" alt="finger pointing right" />
				<p class="text-3xl">suffix</p>
				<Input bind:value={suffix} type="text" class="w-36" />
			{/if}

			<Button variant="ghost" type="submit" class="p-0 underline">search</Button>

			{#if data.pro}
				{@render simple_search()}
			{:else}
				{@render pro_search()}
			{/if}
		</form>
	{:else}
		<p>
			{#if data.cities.length > 0}
				<img src={happy} class="inline-block h-9" alt="happy face" />
			{:else}
				<img src={sad} class="inline-block h-9" alt="sad face" />
			{/if}

			{data.cities.length} out of {data.coordinate_count} german cities<a href="#explainer">*</a>

			{#if data.prefix}
				start{data.cities.length == 1 ? 's' : ''} with "{data.prefix}"
			{/if}
			{#if data.prefix && data.infix}
				and
			{/if}
			{#if data.infix}
				contain{data.cities.length == 1 ? 's' : ''}
				"{data.infix}"
			{/if}
			{#if data.infix && data.suffix}
				and
			{/if}
			{#if data.prefix && data.suffix && !data.infix}
				and
			{/if}
			{#if data.suffix}
				end{data.cities.length == 1 ? 's' : ''} with "{data.suffix}"
			{/if}
			{#if data.cities.length > 0}
				<img src={happy} class="inline-block h-9" alt="happy face" />
			{:else}
				<img src={sad} class="inline-block h-9" alt="sad face" />
			{/if}
			new search:
			{@render simple_search()}
			or
			{@render pro_search()}
		</p>
	{/if}
</div>
