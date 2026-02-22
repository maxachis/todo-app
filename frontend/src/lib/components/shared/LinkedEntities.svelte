<script lang="ts">
	let {
		label,
		entities,
		linkedIds,
		getDisplayName,
		onAdd,
		onRemove
	}: {
		label: string;
		entities: { id: number }[];
		linkedIds: number[];
		getDisplayName: (entity: { id: number }) => string;
		onAdd: (id: number) => void;
		onRemove: (id: number) => void;
	} = $props();

	let selectedId = $state('');

	const available = $derived(
		entities.filter((e) => !linkedIds.includes(e.id))
	);

	const linked = $derived(
		linkedIds
			.map((id) => entities.find((e) => e.id === id))
			.filter((e): e is { id: number } => e !== undefined)
	);

	function handleAdd() {
		if (selectedId) {
			onAdd(Number(selectedId));
			selectedId = '';
		}
	}
</script>

<div class="linked-entities">
	<span class="linked-label">{label}</span>
	{#if linked.length > 0}
		<ul class="linked-list">
			{#each linked as entity (entity.id)}
				<li class="linked-item">
					<span class="linked-name">{getDisplayName(entity)}</span>
					<button class="remove-btn" onclick={() => onRemove(entity.id)} aria-label="Remove {getDisplayName(entity)}">&times;</button>
				</li>
			{/each}
		</ul>
	{/if}
	{#if available.length > 0}
		<div class="add-row">
			<select bind:value={selectedId} class="add-select">
				<option value="">Add {label.toLowerCase()}...</option>
				{#each available as entity (entity.id)}
					<option value={entity.id}>{getDisplayName(entity)}</option>
				{/each}
			</select>
			<button class="add-btn" onclick={handleAdd} disabled={!selectedId}>+</button>
		</div>
	{/if}
</div>

<style>
	.linked-entities {
		margin-top: 0.5rem;
	}

	.linked-label {
		font-size: 0.78rem;
		font-weight: 600;
		color: var(--text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.03em;
	}

	.linked-list {
		list-style: none;
		margin: 0.35rem 0 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	.linked-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.25rem 0.4rem;
		border-radius: var(--radius-sm);
		font-size: 0.83rem;
		color: var(--text-primary);
		transition: background var(--transition);
	}

	.linked-item:hover {
		background: var(--bg-surface-hover);
	}

	.linked-name {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		min-width: 0;
	}

	.remove-btn {
		background: transparent;
		border: none;
		cursor: pointer;
		font-size: 1rem;
		line-height: 1;
		color: var(--text-tertiary);
		padding: 0 0.25rem;
		border-radius: var(--radius-sm);
		transition: color var(--transition);
		flex-shrink: 0;
	}

	.remove-btn:hover {
		color: var(--error);
	}

	.add-row {
		display: flex;
		gap: 0.3rem;
		margin-top: 0.35rem;
	}

	.add-select {
		flex: 1;
		min-width: 0;
		font-size: 0.8rem;
		font-family: var(--font-body);
		padding: 0.25rem 0.4rem;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.add-btn {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.2rem 0.5rem;
		cursor: pointer;
		font-size: 0.9rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.add-btn:hover:not(:disabled) {
		border-color: var(--accent);
		color: var(--accent);
	}

	.add-btn:disabled {
		opacity: 0.4;
		cursor: default;
	}
</style>
