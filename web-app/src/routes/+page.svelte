<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<ul>
	{#each data.rows as row}
		<li>{row.name}</li>
	{/each}
</ul>
