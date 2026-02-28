<script lang="ts">
	import { page } from '$app/stores';

	let { children } = $props();

	const tabs = [
		{ href: '/network/relationships', label: 'Relationships' },
		{ href: '/network/graph', label: 'Graph' }
	];
</script>

<div class="network-layout">
	<nav class="sub-tabs">
		{#each tabs as tab}
			<a href={tab.href} class:active={$page.url.pathname === tab.href}>{tab.label}</a>
		{/each}
	</nav>
	{@render children()}
</div>

<style>
	.network-layout {
		display: grid;
		grid-template-rows: auto 1fr;
		gap: 0.75rem;
		height: 100%;
		min-height: 0;
	}

	.sub-tabs {
		display: flex;
		gap: 0.25rem;
		background: var(--bg-surface-hover);
		border-radius: var(--radius-md);
		padding: 0.2rem;
		width: fit-content;
	}

	.sub-tabs a {
		text-decoration: none;
		font-family: var(--font-body);
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--text-secondary);
		padding: 0.35rem 0.75rem;
		border-radius: var(--radius-sm);
		transition: all var(--transition);
	}

	.sub-tabs a:hover {
		color: var(--text-primary);
	}

	.sub-tabs a.active {
		background: var(--bg-surface);
		color: var(--text-primary);
		font-weight: 600;
		box-shadow: var(--shadow-sm);
	}
</style>
