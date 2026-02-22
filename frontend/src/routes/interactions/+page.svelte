<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Interaction, type InteractionType, type Person, type List } from '$lib';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';

	let interactions: Interaction[] = $state([]);
	let people: Person[] = $state([]);
	let interactionTypes: InteractionType[] = $state([]);
	let selected: Interaction | null = $state(null);
	let linkedTaskIds = $state<number[]>([]);
	let allTasks = $state<{ id: number; title: string }[]>([]);

	let newPersonId = $state<number | null>(null);
	let newTypeId = $state<number | null>(null);
	let newDate = $state('');
	let newNotes = $state('');

	let editPersonId = $state<number | null>(null);
	let editTypeId = $state<number | null>(null);
	let editDate = $state('');
	let editNotes = $state('');

	async function loadData(): Promise<void> {
		people = await api.people.getAll();
		interactionTypes = await api.interactionTypes.getAll();
		interactions = await api.interactions.getAll();
		if (selected) {
			selected = interactions.find((item) => item.id === selected?.id) ?? null;
		}
	}

	onMount(() => {
		loadData();
	});

	function findPerson(id: number): Person | undefined {
		return people.find((person) => person.id === id);
	}

	function findType(id: number): InteractionType | undefined {
		return interactionTypes.find((type) => type.id === id);
	}

	function selectInteraction(item: Interaction): void {
		selected = item;
		editPersonId = item.person_id;
		editTypeId = item.interaction_type_id;
		editDate = item.date;
		editNotes = item.notes;
		loadLinkedTasks(item.id);
	}

	async function loadAllTasks(): Promise<void> {
		const lists: List[] = await api.lists.getAll();
		const flat: { id: number; title: string }[] = [];
		for (const list of lists) {
			for (const section of list.sections) {
				for (const task of section.tasks) {
					flat.push({ id: task.id, title: task.title });
				}
			}
		}
		allTasks = flat;
	}

	async function loadLinkedTasks(interactionId: number): Promise<void> {
		if (allTasks.length === 0) await loadAllTasks();
		const links = await api.taskLinks.interactions.list(interactionId);
		linkedTaskIds = links.map((l) => l.task_id);
	}

	async function addTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.interactions.add(selected.id, taskId);
		linkedTaskIds = [...linkedTaskIds, taskId];
	}

	async function removeTaskLink(taskId: number): Promise<void> {
		if (!selected) return;
		await api.taskLinks.interactions.remove(selected.id, taskId);
		linkedTaskIds = linkedTaskIds.filter((id) => id !== taskId);
	}

	function taskName(t: { id: number }): string {
		return allTasks.find((x) => x.id === t.id)?.title ?? `Task #${t.id}`;
	}

	async function createInteraction(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newPersonId || !newTypeId || !newDate) return;
		const created = await api.interactions.create({
			person_id: newPersonId,
			interaction_type_id: newTypeId,
			date: newDate,
			notes: newNotes
		});
		interactions = [created, ...interactions];
		newPersonId = null;
		newTypeId = null;
		newDate = '';
		newNotes = '';
	}

	async function saveInteraction(): Promise<void> {
		if (!selected || !editPersonId || !editTypeId || !editDate) return;
		const updated = await api.interactions.update(selected.id, {
			person_id: editPersonId,
			interaction_type_id: editTypeId,
			date: editDate,
			notes: editNotes
		});
		interactions = interactions.map((item) => (item.id === updated.id ? updated : item));
		selected = updated;
	}

	async function deleteInteraction(item: Interaction): Promise<void> {
		if (!confirm('Delete this interaction?')) return;
		await api.interactions.remove(item.id);
		interactions = interactions.filter((entry) => entry.id !== item.id);
		if (selected?.id === item.id) {
			selected = null;
		}
	}
</script>

<section class="network-page">
	<header>
		<h1>Interactions</h1>
	</header>

	<div class="network-grid">
		<div class="panel list-panel">
			<form class="create-form" onsubmit={createInteraction}>
				<select bind:value={newPersonId}>
					<option value={null} disabled selected>Person</option>
					{#each people as person (person.id)}
						<option value={person.id}>{person.last_name}, {person.first_name}</option>
					{/each}
				</select>
				<select bind:value={newTypeId}>
					<option value={null} disabled selected>Interaction type</option>
					{#each interactionTypes as type (type.id)}
						<option value={type.id}>{type.name}</option>
					{/each}
				</select>
				<input type="date" bind:value={newDate} />
				<textarea bind:value={newNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Interaction</button>
			</form>

			<div class="list">
				{#each interactions as item (item.id)}
					<button class="list-item" class:active={selected?.id === item.id} onclick={() => selectInteraction(item)}>
						<div class="title">
							{findPerson(item.person_id)?.last_name ?? 'Person'}, {findPerson(item.person_id)?.first_name ?? ''}
						</div>
						<div class="meta">
							{findType(item.interaction_type_id)?.name ?? 'Type'} · {item.date}
						</div>
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{findPerson(selected.person_id)?.last_name}, {findPerson(selected.person_id)?.first_name}</h2>
					<button class="danger" onclick={() => selected && deleteInteraction(selected)}>Delete</button>
				</div>
				<div class="detail-form">
					<label>
						<span>Person</span>
						<select bind:value={editPersonId}>
							{#each people as person (person.id)}
								<option value={person.id}>{person.last_name}, {person.first_name}</option>
							{/each}
						</select>
					</label>
					<label>
						<span>Interaction type</span>
						<select bind:value={editTypeId}>
							{#each interactionTypes as type (type.id)}
								<option value={type.id}>{type.name}</option>
							{/each}
						</select>
					</label>
					<label>
						<span>Date</span>
						<input type="date" bind:value={editDate} />
					</label>
					<label>
						<span>Notes</span>
						<textarea rows="5" bind:value={editNotes}></textarea>
					</label>
					<button class="primary" onclick={saveInteraction}>Save</button>
				</div>
				<div class="linked-tasks-section">
					<LinkedEntities
						label="Linked Tasks"
						entities={allTasks}
						linkedIds={linkedTaskIds}
						getDisplayName={taskName}
						onAdd={addTaskLink}
						onRemove={removeTaskLink}
					/>
				</div>
			{:else}
				<div class="empty-state">Select an interaction to view details.</div>
			{/if}
		</div>
	</div>
</section>

<style>
	.network-page {
		display: grid;
		gap: 1rem;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
	}

	.network-grid {
		display: grid;
		grid-template-columns: minmax(260px, 1fr) minmax(360px, 2fr);
		gap: 1rem;
	}

	.panel {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.9rem;
		box-shadow: var(--shadow-sm);
	}

	.create-form {
		display: grid;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.create-form select,
	.create-form input,
	.create-form textarea {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
	}

	.create-form button,
	.detail-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.75rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		transition: all var(--transition);
	}

	.create-form button:hover,
	.detail-form button:hover {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.list {
		display: grid;
		gap: 0.5rem;
	}

	.list-item {
		text-align: left;
		border: 1px solid var(--border-light);
		border-radius: var(--radius-sm);
		padding: 0.5rem 0.6rem;
		background: var(--bg-surface);
		cursor: pointer;
		transition: background var(--transition), border-color var(--transition);
	}

	.list-item.active {
		background: var(--accent-light);
		border-color: var(--accent);
	}

	.title {
		font-weight: 600;
		color: var(--text-primary);
	}

	.meta {
		font-size: 0.75rem;
		color: var(--text-tertiary);
	}

	.detail-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		margin-bottom: 0.75rem;
	}

	.detail-form {
		display: grid;
		gap: 0.5rem;
	}

	label {
		display: grid;
		gap: 0.25rem;
		font-size: 0.8rem;
		color: var(--text-secondary);
	}

	label input,
	label textarea,
	label select {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
	}

	.detail-form .primary {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.danger {
		border: 1px solid var(--error-border);
		background: var(--error-bg);
		color: var(--error);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.6rem;
		cursor: pointer;
	}

	.linked-tasks-section {
		margin-top: 0.75rem;
		padding-top: 0.75rem;
		border-top: 1px solid var(--border-light);
	}

	.empty-state {
		color: var(--text-tertiary);
		font-size: 0.9rem;
	}

	@media (max-width: 1024px) {
		.network-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
