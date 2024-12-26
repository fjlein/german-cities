<script lang="ts">
	let { data }: { data: { infix: string; prefix: string; suffix: string; cities: City[] } } =
		$props();
</script>

<div
	class="flex flex-wrap gap-2 [&>*]:rounded-md [&>*]:bg-red-100 [&>*]:px-2 [&>*]:py-1 [&>*]:text-2xl [&>*]:font-medium [&>*]:tracking-tight"
>
	{#if data.prefix || data.infix || data.suffix}
		<a class="no-underline" href="/" data-sveltekit-reload
			>{data.cities.length} german cit{data.cities.length == 1 ? 'y' : 'ies'}</a
		>

		{#if data.prefix}
			<p>start{data.cities.length == 1 ? 's' : ''} with</p>
			<p>{data.prefix}</p>
		{/if}
		{#if data.prefix && data.infix}
			<p>and</p>
		{/if}
		{#if data.infix}
			<p>contain{data.cities.length == 1 ? 's' : ''}</p>
			<p>{data.infix}</p>
		{/if}
		{#if data.infix && data.suffix}
			<p>and</p>
		{/if}
		{#if data.prefix && data.suffix && !data.infix}
			<p>and</p>
		{/if}
		{#if data.suffix}
			<p>end{data.cities.length == 1 ? 's' : ''} with</p>
			<p>{data.suffix}</p>
		{/if}
		<!-- {:else}
		<p>simple search</p>
		<p>advanced search</p>
		<p>random</p> -->
	{/if}
</div>
