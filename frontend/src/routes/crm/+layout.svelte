<script lang="ts">
	import { page } from '$app/stores';
	import '$lib/styles/crm.css';

	let { children } = $props();

	const tabs = [
		{ href: '/crm/people', label: 'People' },
		{ href: '/crm/orgs', label: 'Orgs' },
		{ href: '/crm/interactions', label: 'Interactions' },
		{ href: '/crm/leads', label: 'Leads' }
	];
</script>

<div class="crm-layout">
	<nav class="sub-tabs">
		{#each tabs as tab}
			<a href={tab.href} class:active={$page.url.pathname === tab.href}>{tab.label}</a>
		{/each}
	</nav>
	{@render children()}
</div>

<style>
	.crm-layout {
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
