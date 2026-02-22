<script lang="ts">
	import { onMount } from 'svelte';
	import {
		api,
		type Organization,
		type Person,
		type RelationshipOrganizationPerson,
		type RelationshipPersonPerson
	} from '$lib';

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
				<select bind:value={newPerson1Id}>
					<option value={null} disabled selected>Person A</option>
					{#each people as person (person.id)}
						<option value={person.id}>{person.last_name}, {person.first_name}</option>
					{/each}
				</select>
				<select bind:value={newPerson2Id}>
					<option value={null} disabled selected>Person B</option>
					{#each people as person (person.id)}
						<option value={person.id}>{person.last_name}, {person.first_name}</option>
					{/each}
				</select>
				<textarea bind:value={newPersonNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Relationship</button>
			</form>

			<div class="list">
				{#each personRelationships as rel (rel.id)}
					<div class="list-item">
						<div class="title">{personLabel(rel.person_1_id)} ↔ {personLabel(rel.person_2_id)}</div>
						{#if rel.notes}
							<div class="meta">{rel.notes}</div>
						{/if}
						<button class="danger" onclick={() => deletePersonRelationship(rel.id)}>Delete</button>
					</div>
				{/each}
			</div>
		</div>

		<div class="panel">
			<h2>Organization → Person</h2>
			<form class="create-form" onsubmit={createOrgRelationship}>
				<select bind:value={newOrgId}>
					<option value={null} disabled selected>Organization</option>
					{#each organizations as org (org.id)}
						<option value={org.id}>{org.name}</option>
					{/each}
				</select>
				<select bind:value={newOrgPersonId}>
					<option value={null} disabled selected>Person</option>
					{#each people as person (person.id)}
						<option value={person.id}>{person.last_name}, {person.first_name}</option>
					{/each}
				</select>
				<textarea bind:value={newOrgNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Relationship</button>
			</form>

			<div class="list">
				{#each orgRelationships as rel (rel.id)}
					<div class="list-item">
						<div class="title">{orgLabel(rel.organization_id)} → {personLabel(rel.person_id)}</div>
						{#if rel.notes}
							<div class="meta">{rel.notes}</div>
						{/if}
						<button class="danger" onclick={() => deleteOrgRelationship(rel.id)}>Delete</button>
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

	.create-form select,
	.create-form textarea {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
	}

	.create-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
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

	.danger {
		border: 1px solid var(--error-border);
		background: var(--error-bg);
		color: var(--error);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.5rem;
		cursor: pointer;
		justify-self: start;
	}
</style>
