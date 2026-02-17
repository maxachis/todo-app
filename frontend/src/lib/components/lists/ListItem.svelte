<script lang="ts">
	import type { List } from '$lib';

	let {
		list,
		selected = false,
		editingListId = null,
		onStartEdit = (_id: number) => {},
		onStopEdit = (_id: number) => {},
		onEditEmoji = (_id: number) => {},
		onSelect = (_id: number) => {},
		onUpdate = (_id: number, _changes: { name?: string; emoji?: string }) => {},
		onDelete = (_id: number) => {},
		onTaskDrop = (_listId: number, _taskId: number) => {}
	}: {
		list: List;
		selected?: boolean;
		editingListId?: number | null;
		onStartEdit?: (id: number) => void;
		onStopEdit?: (id: number) => void;
		onEditEmoji?: (id: number) => void;
		onSelect?: (id: number) => void;
		onUpdate?: (id: number, changes: { name?: string; emoji?: string }) => void;
		onDelete?: (id: number) => void;
		onTaskDrop?: (listId: number, taskId: number) => void;
	} = $props();

	let name = $state('');
	let wasEditing = $state(false);

	const editing = $derived(editingListId === list.id);

	$effect(() => {
		if (!editing) {
			name = list.name;
		}
	});

	$effect(() => {
		if (editing && !wasEditing) {
			name = list.name;
		}
		if (!editing && wasEditing) {
			commit();
		}
		wasEditing = editing;
	});

	function startEdit(): void {
		onStartEdit(list.id);
	}

	function commit(): void {
		if (name.trim() && name !== list.name) {
			onUpdate(list.id, { name: name.trim() });
		}
		onStopEdit(list.id);
	}
</script>

<div
	class:selected
	class="row"
	data-list-id={list.id}
	role="button"
	tabindex="0"
	ondblclick={startEdit}
	onclick={() => onSelect(list.id)}
	ondragover={(event) => event.preventDefault()}
	ondrop={(event) => {
		event.preventDefault();
		const taskId = Number(event.dataTransfer?.getData('text/task-id'));
		if (!Number.isNaN(taskId)) {
			onTaskDrop(list.id, taskId);
		}
	}}
	onkeydown={(event) => {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			onSelect(list.id);
		}
	}}
>
	<button
		type="button"
		class="emoji-btn"
		ondblclick={(event) => {
			event.preventDefault();
			event.stopPropagation();
			onEditEmoji(list.id);
		}}
		onclick={(event) => {
			event.preventDefault();
			event.stopPropagation();
		}}
		aria-label="Edit list emoji"
	>
		<span class="emoji">{list.emoji || '\u{1F4DD}'}</span>
	</button>
	{#if editing}
		<input
			bind:value={name}
			onblur={commit}
			onkeydown={(event) => {
				if (event.key === 'Enter') commit();
				if (event.key === 'Escape') onStopEdit(list.id);
			}}
		/>
	{:else}
		<span class="name">{list.name}</span>
	{/if}
	<button type="button" class="delete" onclick={(event) => { event.stopPropagation(); onDelete(list.id); }}>&#10005;</button>
</div>

<style>
	.row {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 0.45rem;
		align-items: center;
		padding: 0.5rem 0.55rem;
		border-radius: var(--radius-md);
		cursor: pointer;
		transition: all var(--transition);
	}

	.row:hover {
		background: var(--bg-surface-hover);
	}

	.row.selected {
		background: var(--accent-light);
		box-shadow: inset 3px 0 0 var(--accent);
	}

	.emoji {
		font-size: 1.1rem;
	}

	.emoji-btn {
		border: none;
		background: transparent;
		padding: 0;
		cursor: pointer;
		line-height: 1;
	}

	.name {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		font-size: 0.88rem;
		font-weight: 500;
		color: var(--text-primary);
	}

	input {
		border: 1px solid var(--border-focus);
		border-radius: var(--radius-sm);
		padding: 0.2rem 0.4rem;
		font-family: var(--font-body);
		font-size: 0.88rem;
		color: var(--text-primary);
	}

	input:focus {
		outline: none;
	}

	.delete {
		border: none;
		background: transparent;
		color: var(--text-tertiary);
		cursor: pointer;
		opacity: 0;
		transition: opacity var(--transition), color var(--transition);
	}

	.row:hover .delete {
		opacity: 1;
	}

	.delete:hover {
		color: var(--error);
	}
</style>
