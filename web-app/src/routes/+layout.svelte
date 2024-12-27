<script lang="ts">
	import type { Snippet } from 'svelte';
	import '../app.css';

	let { children }: { children: Snippet } = $props();
</script>

<div class="container my-6 max-w-[600px] px-[8px] sm:mt-16">
	{@render children()}
</div>
