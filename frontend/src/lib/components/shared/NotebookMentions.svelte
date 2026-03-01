<script lang="ts">
	import { api } from '$lib/api';
	import type { PageBacklink } from '$lib/api/types';

	let {
		entityType,
		entityId
	}: {
		entityType: string;
		entityId: number;
	} = $props();

	let mentions = $state<PageBacklink[]>([]);
	let collapsed = $state(false);

	$effect(() => {
		if (entityType && entityId) {
			api.notebook.mentions(entityType, entityId).then((data) => {
				mentions = data;
			});
		}
	});
</script>

{#if mentions.length > 0}
	<div class="notebook-mentions">
		<button class="mentions-header" onclick={() => (collapsed = !collapsed)}>
			<span class="toggle">{collapsed ? '\u25B6' : '\u25BC'}</span>
			<span class="mentions-title">Notebook Mentions ({mentions.length})</span>
		</button>
		{#if !collapsed}
			<div class="mentions-list">
				{#each mentions as m (m.id)}
					<a href="/notebook?p={m.slug}" class="mention-item">
						<span class="mention-icon">{m.page_type === 'daily' ? '\u{1F4C5}' : '\u{1F4C4}'}</span>
						<span class="mention-title">{m.title}</span>
						<span class="mention-snippet">{m.snippet}</span>
					</a>
				{/each}
			</div>
		{/if}
	</div>
{/if}

<style>
	.notebook-mentions {
		margin-top: 0.75rem;
		padding-top: 0.5rem;
		border-top: 1px solid var(--border-light);
	}

	.mentions-header {
		display: flex;
		align-items: center;
		gap: 0.35rem;
		background: none;
		border: none;
		cursor: pointer;
		padding: 0.2rem 0;
		font-family: var(--font-body);
		width: 100%;
		text-align: left;
	}

	.toggle {
		font-size: 0.65rem;
		color: var(--text-tertiary);
	}

	.mentions-title {
		font-size: 0.8rem;
		font-weight: 600;
		color: var(--text-secondary);
	}

	.mentions-list {
		margin-top: 0.35rem;
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
	}

	.mention-item {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0.3rem 0.4rem;
		border-radius: var(--radius-sm);
		text-decoration: none;
		transition: background var(--transition);
	}

	.mention-item:hover {
		background: var(--bg-surface-hover);
	}

	.mention-icon {
		font-size: 0.8rem;
		flex-shrink: 0;
	}

	.mention-title {
		font-size: 0.82rem;
		font-weight: 600;
		color: var(--accent);
		white-space: nowrap;
		flex-shrink: 0;
	}

	.mention-snippet {
		font-size: 0.75rem;
		color: var(--text-tertiary);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
</style>
