<script lang="ts">
	import type { SearchResponse } from '$lib';
	import { selectList } from '$lib/stores/lists';
	import { selectTask } from '$lib/stores/tasks';

	let {
		results,
		onNavigate = () => {}
	}: {
		results: SearchResponse;
		onNavigate?: () => void;
	} = $props();

	async function navigateTo(listId: number, taskId: number): Promise<void> {
		await selectList(listId);
		await selectTask(taskId);
		onNavigate();
	}
</script>

<div class="results-dropdown">
	{#if results.total_count === 0}
		<div class="no-results">No results for "{results.query}"</div>
	{:else}
		{#each results.results as group}
			<div class="group">
				<div class="group-header">{group.list.emoji || '📝'} {group.list.name}</div>
				{#each group.tasks as task}
					<button class="result" onclick={() => navigateTo(group.list.id, task.id)}>
						<span class="result-title">{task.title}</span>
						<span class="result-section">{task.section_name}</span>
						{#if task.tags.length > 0}
							<span class="result-tags">
								{#each task.tags as tag}
									<span class="tag">{tag}</span>
								{/each}
							</span>
						{/if}
					</button>
				{/each}
			</div>
		{/each}
	{/if}
</div>

<style>
	.results-dropdown {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		min-width: 300px;
		max-height: 400px;
		overflow-y: auto;
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-lg);
		z-index: 50;
		margin-top: 0.4rem;
	}

	.no-results {
		padding: 0.75rem 1rem;
		color: var(--text-tertiary);
		font-size: 0.85rem;
		font-style: italic;
	}

	.group {
		border-bottom: 1px solid var(--border-light);
	}

	.group:last-child {
		border-bottom: none;
	}

	.group-header {
		padding: 0.55rem 0.75rem 0.25rem;
		font-size: 0.7rem;
		font-weight: 600;
		color: var(--text-tertiary);
		text-transform: uppercase;
		letter-spacing: 0.06em;
	}

	.result {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.3rem;
		width: 100%;
		background: transparent;
		border: none;
		cursor: pointer;
		padding: 0.45rem 0.75rem;
		text-align: left;
		font-family: var(--font-body);
		transition: background var(--transition);
	}

	.result:hover {
		background: var(--bg-surface-hover);
	}

	.result-title {
		font-size: 0.85rem;
		color: var(--text-primary);
	}

	.result-section {
		font-size: 0.7rem;
		color: var(--text-tertiary);
		grid-column: 2;
		grid-row: 1;
	}

	.result-tags {
		grid-column: 1 / -1;
		display: flex;
		gap: 0.2rem;
	}

	.tag {
		background: var(--tag-bg);
		color: var(--tag-text);
		padding: 0.05rem 0.3rem;
		border-radius: var(--radius-sm);
		font-size: 0.65rem;
		font-weight: 500;
	}
</style>
