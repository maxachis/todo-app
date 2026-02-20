<script lang="ts">
	import { dndzone } from 'svelte-dnd-action';

	import { api, type List } from '$lib';
	import { listsStore, selectedListStore, createList, deleteList, loadLists, selectList, updateList } from '$lib/stores/lists';
	import { moveTask } from '$lib/stores/tasks';
	import { addToast } from '$lib/stores/toast';
	import EmojiPicker from './EmojiPicker.svelte';
	import ListItem from './ListItem.svelte';
	import ExportButton from '../shared/ExportButton.svelte';

	let creatingName = $state('');
	let creatingEmoji = $state('\u{1F4DD}');
	let emojiPickerOpen = $state(false);
	let editingEmojiListId = $state<number | null>(null);
	let sortableLists = $state<List[]>([]);
	let editingListId = $state<number | null>(null);

	$effect(() => {
		loadLists();
	});

	$effect(() => {
		sortableLists = [...$listsStore];
	});

	async function submitCreate(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		const name = creatingName.trim();
		if (!name) return;
		await createList({ name, emoji: creatingEmoji });
		creatingName = '';
	}

	async function handleDelete(listId: number): Promise<void> {
		if (!confirm('Delete this list?')) return;
		await deleteList(listId);
	}

	function handleConsider(event: CustomEvent<{ items: List[] }>): void {
		sortableLists = event.detail.items as List[];
	}

	async function handleReorder(event: CustomEvent<{ items: List[] }>): Promise<void> {
		const previous = [...$listsStore];
		sortableLists = event.detail.items as List[];
		listsStore.set(sortableLists);
		try {
			for (let i = 0; i < sortableLists.length; i += 1) {
				await api.lists.move(sortableLists[i].id, { position: i });
			}
			await loadLists();
		} catch {
			listsStore.set(previous);
			sortableLists = previous;
			addToast({ message: 'List reorder failed. Changes reverted.', type: 'error' });
		}
	}

	async function handleTaskDrop(targetListId: number, taskId: number): Promise<void> {
		try {
			await moveTask(taskId, { list_id: targetListId });
			addToast({ message: 'Task moved to list', type: 'success' });
		} catch {
			addToast({ message: 'Unable to move task to list', type: 'error' });
		}
	}

	function handleStartEdit(listId: number): void {
		editingListId = listId;
	}

	function handleStopEdit(listId: number): void {
		if (editingListId === listId) {
			editingListId = null;
		}
	}

	function handleEditEmoji(listId: number): void {
		editingEmojiListId = listId;
	}

	async function handleSelectListEmoji(emoji: string): Promise<void> {
		if (editingEmojiListId === null) return;
		await updateList(editingEmojiListId, { emoji });
		editingEmojiListId = null;
	}
</script>

<section class="sidebar">
	<header>
		<h2>Lists</h2>
		<ExportButton label="Export All" />
	</header>

	<form onsubmit={submitCreate} class="create-form">
		<button type="button" class="emoji" onclick={() => (emojiPickerOpen = true)}>{creatingEmoji}</button>
		<input bind:value={creatingName} placeholder="Create list..." />
		<button type="submit">Add</button>
	</form>

	<div class="list-dnd-zone" use:dndzone={{ items: sortableLists, flipDurationMs: 150 }} onconsider={handleConsider} onfinalize={handleReorder}>
		{#each sortableLists as list (list.id)}
			<ListItem
				{list}
				selected={$selectedListStore === list.id}
				{editingListId}
				onStartEdit={handleStartEdit}
				onStopEdit={handleStopEdit}
				onEditEmoji={handleEditEmoji}
				onSelect={selectList}
				onUpdate={(id, changes) => updateList(id, changes)}
				onDelete={handleDelete}
				onTaskDrop={handleTaskDrop}
			/>
		{/each}
	</div>
</section>

<EmojiPicker
	open={emojiPickerOpen}
	onClose={() => (emojiPickerOpen = false)}
	onSelect={(emoji) => (creatingEmoji = emoji)}
/>

<EmojiPicker
	open={editingEmojiListId !== null}
	onClose={() => (editingEmojiListId = null)}
	onSelect={handleSelectListEmoji}
/>

<style>
	.sidebar {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
		height: 100%;
		min-height: 0;
	}

	.list-dnd-zone {
		flex: 1;
		overflow-y: auto;
		min-height: 0;
	}

	h2 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.create-form {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 0.35rem;
	}

	input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.55rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-primary);
		background: var(--bg-input);
		transition: border-color var(--transition);
	}

	input::placeholder {
		color: var(--text-tertiary);
	}

	input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.6rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.82rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.emoji {
		font-size: 1rem;
	}
</style>
