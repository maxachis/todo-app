<script lang="ts">
	import { page } from '$app/stores';
	import { setContext } from 'svelte';
	import '$lib/styles/crm.css';
	import { api } from '$lib/api';

	let { children } = $props();

	let inboxCount = $state(0);

	const tabs = [
		{ href: '/crm/inbox', label: 'Inbox' },
		{ href: '/crm/people', label: 'People' },
		{ href: '/crm/orgs', label: 'Orgs' },
		{ href: '/crm/interactions', label: 'Interactions' },
		{ href: '/crm/leads', label: 'Leads' },
		{ href: '/crm/relationships', label: 'Relationships' }
	];

	async function refreshInboxCount() {
		try {
			const drafts = await api.contactDrafts.list();
			inboxCount = drafts.length;
		} catch {
			inboxCount = 0;
		}
	}

	setContext('refreshInboxCount', refreshInboxCount);

	$effect(() => {
		$page.url.pathname;
		refreshInboxCount();
	});
</script>

<div class="crm-layout">
	<nav class="sub-tabs">
		{#each tabs as tab}
			<a href={tab.href} class:active={$page.url.pathname === tab.href}>{tab.label}{#if tab.href === '/crm/inbox' && inboxCount > 0} <span class="badge">{inboxCount}</span>{/if}</a>
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

	.badge {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 1.1rem;
		height: 1.1rem;
		padding: 0 0.3rem;
		font-size: 0.65rem;
		font-weight: 600;
		border-radius: 999px;
		background: var(--accent);
		color: white;
		margin-left: 0.2rem;
	}
</style>
