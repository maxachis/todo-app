<script lang="ts">
	import { onMount } from 'svelte';
	import {
		api,
		type Organization,
		type Person,
		type RelationshipOrganizationPerson,
		type RelationshipPersonPerson
	} from '$lib';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';

	let people: Person[] = $state([]);
	let organizations: Organization[] = $state([]);
	let personRelationships: RelationshipPersonPerson[] = $state([]);
	let orgRelationships: RelationshipOrganizationPerson[] = $state([]);

	let newPerson1Id = $state<number | null>(null);
	let newPerson2Id = $state<number | null>(null);
	let newPersonNotes = $state('');

	let newOrgId = $state<number | null>(null);
	let newOrgPersonId = $state<number | null>(null);
	let newOrgNotes = $state('');

	let editingId = $state<number | null>(null);
	let editingType = $state<'person' | 'org' | null>(null);
	let editingNotes = $state('');

	function startEdit(id: number, type: 'person' | 'org', currentNotes: string): void {
		editingId = id;
		editingType = type;
		editingNotes = currentNotes;
	}

	function cancelEdit(): void {
		editingId = null;
		editingType = null;
		editingNotes = '';
	}

	async function saveEdit(): Promise<void> {
		if (editingId === null || editingType === null) return;
		const id = editingId;
		const notes = editingNotes;
		const type = editingType;
		cancelEdit();
		if (type === 'person') {
			const updated = await api.relationships.people.update(id, { notes });
			personRelationships = personRelationships.map((r) => (r.id === id ? updated : r));
		} else {
			const updated = await api.relationships.organizations.update(id, { notes });
			orgRelationships = orgRelationships.map((r) => (r.id === id ? updated : r));
		}
	}

	function handleEditKeydown(event: KeyboardEvent): void {
		if (event.key === 'Escape') {
			cancelEdit();
		}
	}

	function autofocus(node: HTMLTextAreaElement): void {
		node.focus();
	}

	async function loadData(): Promise<void> {
		people = await api.people.getAll();
		organizations = await api.organizations.getAll();
		personRelationships = await api.relationships.people.getAll();
		orgRelationships = await api.relationships.organizations.getAll();
	}

	onMount(() => {
		loadData();
	});

	function personLabel(id: number): string {
		const person = people.find((item) => item.id === id);
		return person ? `${person.last_name}, ${person.first_name}` : 'Unknown';
	}

	function orgLabel(id: number): string {
		const org = organizations.find((item) => item.id === id);
		return org ? org.name : 'Unknown';
	}

	async function createPersonRelationship(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newPerson1Id || !newPerson2Id) return;
		const created = await api.relationships.people.create({
			person_1_id: newPerson1Id,
			person_2_id: newPerson2Id,
			notes: newPersonNotes
		});
		personRelationships = [...personRelationships, created];
		newPerson1Id = null;
		newPerson2Id = null;
		newPersonNotes = '';
	}

	async function createOrgRelationship(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newOrgId || !newOrgPersonId) return;
		const created = await api.relationships.organizations.create({
			organization_id: newOrgId,
			person_id: newOrgPersonId,
			notes: newOrgNotes
		});
		orgRelationships = [...orgRelationships, created];
		newOrgId = null;
		newOrgPersonId = null;
		newOrgNotes = '';
	}

	async function deletePersonRelationship(id: number): Promise<void> {
		if (!confirm('Delete this relationship?')) return;
		await api.relationships.people.remove(id);
		personRelationships = personRelationships.filter((item) => item.id !== id);
	}

	async function deleteOrgRelationship(id: number): Promise<void> {
		if (!confirm('Delete this relationship?')) return;
		await api.relationships.organizations.remove(id);
		orgRelationships = orgRelationships.filter((item) => item.id !== id);
	}
</script>

<section class="network-page">
	<header>
		<h1>Relationships</h1>
	</header>

	<div class="network-grid">
		<div class="panel">
			<h2>Person ↔ Person</h2>
			<form class="create-form" onsubmit={createPersonRelationship}>
				<TypeaheadSelect
					options={people.map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))}
					placeholder="Person A"
					bind:value={newPerson1Id}
				/>
				<TypeaheadSelect
					options={people.map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))}
					placeholder="Person B"
					bind:value={newPerson2Id}
				/>
				<textarea bind:value={newPersonNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Relationship</button>
			</form>

			<div class="list">
				{#each personRelationships as rel (rel.id)}
					<div class="list-item">
						<div class="title">{personLabel(rel.person_1_id)} ↔ {personLabel(rel.person_2_id)}</div>
						{#if editingId === rel.id && editingType === 'person'}
							<textarea
								class="edit-notes"
								bind:value={editingNotes}
								onblur={saveEdit}
								onkeydown={handleEditKeydown}
								use:autofocus
							></textarea>
						{:else}
							<button class="notes-btn" onclick={() => startEdit(rel.id, 'person', rel.notes || '')}>
								{#if rel.notes}
									<span class="meta">{rel.notes}</span>
								{:else}
									<span class="meta placeholder">&#9998; Add notes</span>
								{/if}
							</button>
						{/if}
						<div class="actions">
							<button class="danger" onclick={() => deletePersonRelationship(rel.id)}>Delete</button>
						</div>
					</div>
				{/each}
			</div>
		</div>

		<div class="panel">
			<h2>Organization → Person</h2>
			<form class="create-form" onsubmit={createOrgRelationship}>
				<TypeaheadSelect
					options={organizations.map((o) => ({ id: o.id, label: o.name }))}
					placeholder="Organization"
					bind:value={newOrgId}
				/>
				<TypeaheadSelect
					options={people.map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))}
					placeholder="Person"
					bind:value={newOrgPersonId}
				/>
				<textarea bind:value={newOrgNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Relationship</button>
			</form>

			<div class="list">
				{#each orgRelationships as rel (rel.id)}
					<div class="list-item">
						<div class="title">{orgLabel(rel.organization_id)} → {personLabel(rel.person_id)}</div>
						{#if editingId === rel.id && editingType === 'org'}
							<textarea
								class="edit-notes"
								bind:value={editingNotes}
								onblur={saveEdit}
								onkeydown={handleEditKeydown}
								use:autofocus
							></textarea>
						{:else}
							<button class="notes-btn" onclick={() => startEdit(rel.id, 'org', rel.notes || '')}>
								{#if rel.notes}
									<span class="meta">{rel.notes}</span>
								{:else}
									<span class="meta placeholder">&#9998; Add notes</span>
								{/if}
							</button>
						{/if}
						<div class="actions">
							<button class="danger" onclick={() => deleteOrgRelationship(rel.id)}>Delete</button>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</section>

<style>
	.network-page {
		display: grid;
		gap: 1rem;
		height: 100%;
		min-height: 0;
		grid-template-rows: auto 1fr;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
	}

	h2 {
		margin: 0 0 0.5rem;
		font-family: var(--font-display);
		font-size: 1.1rem;
	}

	.network-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 1rem;
		min-height: 0;
	}

	.panel {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.9rem;
		box-shadow: var(--shadow-sm);
		display: grid;
		gap: 0.75rem;
		min-height: 0;
		overflow-y: auto;
	}

	.create-form {
		display: grid;
		gap: 0.5rem;
	}

	.create-form textarea {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.4rem;
		font-family: var(--font-body);
		font-size: 0.8rem;
		background: var(--bg-input);
		color: var(--text-primary);
	}

	.create-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		color: var(--text-primary);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.75rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		transition: all var(--transition);
	}

	.create-form button:hover {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.list {
		display: grid;
		gap: 0.6rem;
	}

	.list-item {
		border: 1px solid var(--border-light);
		border-radius: var(--radius-sm);
		padding: 0.6rem;
		display: grid;
		gap: 0.35rem;
	}

	.title {
		font-weight: 600;
		color: var(--text-primary);
	}

	.meta {
		font-size: 0.75rem;
		color: var(--text-tertiary);
	}

	.notes-btn {
		all: unset;
		cursor: pointer;
		display: block;
		width: 100%;
		border-bottom: 1px dashed var(--border, rgba(0, 0, 0, 0.15));
		padding: 0.25rem 0.4rem;
		border-radius: var(--radius-sm) var(--radius-sm) 0 0;
		transition: background 0.15s, border-color 0.15s;
	}

	.notes-btn:hover {
		background: var(--bg-hover, rgba(0, 0, 0, 0.04));
		border-bottom-color: var(--accent, #4a90d9);
	}

	.notes-btn:focus-visible {
		outline: 2px solid var(--accent, #4a90d9);
		outline-offset: 1px;
		border-radius: var(--radius-sm);
	}

	.placeholder {
		font-style: italic;
		color: var(--text-quaternary, var(--text-tertiary));
		opacity: 0.7;
	}

	.edit-notes {
		border: 1px solid var(--accent);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		resize: vertical;
		min-height: 2.5rem;
	}

	.actions {
		display: flex;
		gap: 0.35rem;
	}

	.danger {
		border: 1px solid var(--error-border);
		background: var(--error-bg);
		color: var(--error);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.5rem;
		cursor: pointer;
	}
</style>
