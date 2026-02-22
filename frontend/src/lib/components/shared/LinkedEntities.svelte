<script lang="ts">
	import TypeaheadSelect from './TypeaheadSelect.svelte';

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

	const available = $derived(
		entities.filter((e) => !linkedIds.includes(e.id))
	);

	const typeaheadOptions = $derived(
		available.map((e) => ({ id: e.id, label: getDisplayName(e) }))
	);

	const linked = $derived(
		linkedIds
			.map((id) => entities.find((e) => e.id === id))
			.filter((e): e is { id: number } => e !== undefined)
	);
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
	{#if typeaheadOptions.length > 0}
		<div class="add-row">
			<TypeaheadSelect
				options={typeaheadOptions}
				placeholder="Add {label.toLowerCase()}..."
				onSelect={onAdd}
			/>
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

</style>
