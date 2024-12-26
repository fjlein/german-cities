<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { navigating, page } from '$app/state';
	import Button from './ui/button/button.svelte';
	import { Input } from './ui/input';
	import Search from 'lucide-svelte/icons/search';

	let prefix = $state(page.data.prefix);
	let infix = $state(page.data.infix);
	let suffix = $state(page.data.suffix);

	function search() {
		let query = page.url.searchParams;
		query.set('prefix', prefix);
		query.set('infix', infix);
		query.set('suffix', suffix);
		goto(`${page.url.origin}?${query.toString()}`, { invalidateAll: true });
	}
</script>

<div>
	<form
		class="flex gap-2"
		onsubmit={(event) => {
			event.preventDefault();
			search();
		}}
	>
		<Input placeholder="prefix" bind:value={prefix} type="text" />
		<Input placeholder="infix" bind:value={infix} type="text" />
		<Input placeholder="suffix" bind:value={suffix} type="text" />
		<Button variant="outline" type="submit"><Search /></Button>
	</form>
</div>
