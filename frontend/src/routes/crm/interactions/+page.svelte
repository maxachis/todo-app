<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Interaction, type InteractionMedium, type InteractionType, type Person, type Organization } from '$lib';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';
	import { createLinkedTasksManager } from '$lib/components/shared/linkedTasks.svelte';

	const ltm = createLinkedTasksManager('interactions');

	let interactions: Interaction[] = $state([]);
	let people: Person[] = $state([]);
	let organizations: Organization[] = $state([]);
	let interactionTypes: InteractionType[] = $state([]);
	let interactionMediums: InteractionMedium[] = $state([]);
	let selected: Interaction | null = $state(null);

	let newPersonIds = $state<number[]>([]);
	let newOrgIds = $state<number[]>([]);
	let newTypeId = $state<number | null>(null);
	let newMediumId = $state<number | null>(null);
	let newDate = $state('');
	let newNotes = $state('');

	let editPersonIds = $state<number[]>([]);
	let editOrgIds = $state<number[]>([]);
	let editTypeId = $state<number | null>(null);
	let editMediumId = $state<number | null>(null);
	let editDate = $state('');
	let editNotes = $state('');

	async function loadData(): Promise<void> {
		people = await api.people.getAll();
		organizations = await api.organizations.getAll();
		interactionTypes = await api.interactionTypes.getAll();
		interactionMediums = await api.interactionMediums.getAll();
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

	function personLabel(id: number): string {
		const p = findPerson(id);
		return p ? `${p.last_name}, ${p.first_name}` : `Person #${id}`;
	}

	function formatPeopleNames(personIds: number[]): string {
		if (personIds.length === 0) return 'No people';
		const names = personIds.map((id) => personLabel(id));
		if (names.length <= 3) return names.join('; ');
		return `${names.slice(0, 2).join('; ')} +${names.length - 2} more`;
	}

	function findOrg(id: number): Organization | undefined {
		return organizations.find((org) => org.id === id);
	}

	function orgLabel(id: number): string {
		return findOrg(id)?.name ?? `Org #${id}`;
	}

	function formatOrgNames(orgIds: number[]): string {
		return orgIds.map((id) => orgLabel(id)).join('; ');
	}

	function findType(id: number): InteractionType | undefined {
		return interactionTypes.find((type) => type.id === id);
	}

	function findMedium(id: number): InteractionMedium | undefined {
		return interactionMediums.find((m) => m.id === id);
	}

	function selectInteraction(item: Interaction): void {
		selected = item;
		editPersonIds = [...item.person_ids];
		editOrgIds = [...item.organization_ids];
		editTypeId = item.interaction_type_id;
		editMediumId = item.interaction_medium_id;
		editDate = item.date;
		editNotes = item.notes;
		ltm.loadLinkedTasks(item.id);
	}

	function addTaskLink(taskId: number): void {
		if (selected) ltm.addTaskLink(selected.id, taskId);
	}

	function removeTaskLink(taskId: number): void {
		if (selected) ltm.removeTaskLink(selected.id, taskId);
	}

	async function handleCreateInteractionType(name: string): Promise<{ id: number; label: string }> {
		const created = await api.interactionTypes.create({ name });
		interactionTypes = [...interactionTypes, created].sort((a, b) => a.name.localeCompare(b.name));
		return { id: created.id, label: created.name };
	}

	async function handleCreateInteractionMedium(name: string): Promise<{ id: number; label: string }> {
		const created = await api.interactionMediums.create({ name });
		interactionMediums = [...interactionMediums, created].sort((a, b) => a.name.localeCompare(b.name));
		return { id: created.id, label: created.name };
	}

	function addNewPerson(id: number): void {
		if (!newPersonIds.includes(id)) {
			newPersonIds = [...newPersonIds, id];
		}
	}

	function removeNewPerson(id: number): void {
		newPersonIds = newPersonIds.filter((pid) => pid !== id);
	}

	function addEditPerson(id: number): void {
		if (!editPersonIds.includes(id)) {
			editPersonIds = [...editPersonIds, id];
		}
	}

	function removeEditPerson(id: number): void {
		editPersonIds = editPersonIds.filter((pid) => pid !== id);
	}

	function addNewOrg(id: number): void {
		if (!newOrgIds.includes(id)) {
			newOrgIds = [...newOrgIds, id];
		}
	}

	function removeNewOrg(id: number): void {
		newOrgIds = newOrgIds.filter((oid) => oid !== id);
	}

	function addEditOrg(id: number): void {
		if (!editOrgIds.includes(id)) {
			editOrgIds = [...editOrgIds, id];
		}
	}

	function removeEditOrg(id: number): void {
		editOrgIds = editOrgIds.filter((oid) => oid !== id);
	}

	async function createInteraction(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (newPersonIds.length === 0 || !newTypeId || !newDate) return;
		const created = await api.interactions.create({
			person_ids: newPersonIds,
			organization_ids: newOrgIds,
			interaction_type_id: newTypeId,
			interaction_medium_id: newMediumId,
			date: newDate,
			notes: newNotes
		});
		interactions = [created, ...interactions];
		newPersonIds = [];
		newOrgIds = [];
		newTypeId = null;
		newMediumId = null;
		newDate = '';
		newNotes = '';
	}

	async function saveInteraction(): Promise<void> {
		if (!selected || editPersonIds.length === 0 || !editTypeId || !editDate) return;
		const updated = await api.interactions.update(selected.id, {
			person_ids: editPersonIds,
			organization_ids: editOrgIds,
			interaction_type_id: editTypeId,
			interaction_medium_id: editMediumId,
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

<section class="crm-page">
	<header>
		<h1>Interactions</h1>
	</header>

	<div class="crm-grid">
		<div class="panel list-panel">
			<form class="create-form" onsubmit={createInteraction}>
				<div class="people-select">
					<TypeaheadSelect
						options={people.filter((p) => !newPersonIds.includes(p.id)).map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))}
						placeholder="Add person..."
						onSelect={addNewPerson}
					/>
					{#if newPersonIds.length > 0}
						<div class="chips">
							{#each newPersonIds as pid (pid)}
								<span class="chip">
									{personLabel(pid)}
									<button type="button" class="chip-remove" onclick={() => removeNewPerson(pid)}>&times;</button>
								</span>
							{/each}
						</div>
					{/if}
				</div>
				<div class="people-select">
					<TypeaheadSelect
						options={organizations.filter((o) => !newOrgIds.includes(o.id)).map((o) => ({ id: o.id, label: o.name }))}
						placeholder="Add organization..."
						onSelect={addNewOrg}
					/>
					{#if newOrgIds.length > 0}
						<div class="chips">
							{#each newOrgIds as oid (oid)}
								<span class="chip">
									{orgLabel(oid)}
									<button type="button" class="chip-remove" onclick={() => removeNewOrg(oid)}>&times;</button>
								</span>
							{/each}
						</div>
					{/if}
				</div>
				<TypeaheadSelect
					options={interactionTypes.map((t) => ({ id: t.id, label: t.name }))}
					placeholder="Interaction type"
					bind:value={newTypeId}
					onCreate={handleCreateInteractionType}
				/>
				<TypeaheadSelect
					options={interactionMediums.map((m) => ({ id: m.id, label: m.name }))}
					placeholder="Medium"
					bind:value={newMediumId}
					onCreate={handleCreateInteractionMedium}
				/>
				<input type="date" bind:value={newDate} />
				<textarea bind:value={newNotes} placeholder="Notes" onkeydown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); e.currentTarget.closest('form')?.requestSubmit(); } }}></textarea>
				<button type="submit">+ Interaction</button>
			</form>

			<div class="list">
				{#each interactions as item (item.id)}
					<button class="list-item" class:active={selected?.id === item.id} onclick={() => selectInteraction(item)}>
						<div class="title">
							{formatPeopleNames(item.person_ids)}
						</div>
						{#if item.organization_ids.length > 0}
							<div class="org-names">{formatOrgNames(item.organization_ids)}</div>
						{/if}
						<div class="meta">
							{findType(item.interaction_type_id)?.name ?? 'Type'}{item.interaction_medium_id ? ` · ${findMedium(item.interaction_medium_id)?.name ?? 'Medium'}` : ''} · {item.date}
						</div>
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{formatPeopleNames(selected.person_ids)}</h2>
					<button class="danger" onclick={() => selected && deleteInteraction(selected)}>Delete</button>
				</div>
				<div class="detail-form">
					<div class="field-group">
						<span class="field-label">People</span>
						<TypeaheadSelect
							options={people.filter((p) => !editPersonIds.includes(p.id)).map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))}
							placeholder="Add person..."
							onSelect={addEditPerson}
						/>
						{#if editPersonIds.length > 0}
							<div class="chips">
								{#each editPersonIds as pid (pid)}
									<span class="chip">
										{personLabel(pid)}
										<button type="button" class="chip-remove" onclick={() => removeEditPerson(pid)}>&times;</button>
									</span>
								{/each}
							</div>
						{/if}
					</div>
					<div class="field-group">
						<span class="field-label">Organizations</span>
						<TypeaheadSelect
							options={organizations.filter((o) => !editOrgIds.includes(o.id)).map((o) => ({ id: o.id, label: o.name }))}
							placeholder="Add organization..."
							onSelect={addEditOrg}
						/>
						{#if editOrgIds.length > 0}
							<div class="chips">
								{#each editOrgIds as oid (oid)}
									<span class="chip">
										{orgLabel(oid)}
										<button type="button" class="chip-remove" onclick={() => removeEditOrg(oid)}>&times;</button>
									</span>
								{/each}
							</div>
						{/if}
					</div>
					<label>
						<span>Interaction type</span>
						<TypeaheadSelect
							options={interactionTypes.map((t) => ({ id: t.id, label: t.name }))}
							placeholder="Interaction type"
							bind:value={editTypeId}
							onCreate={handleCreateInteractionType}
						/>
					</label>
					<label>
						<span>Medium</span>
						<TypeaheadSelect
							options={interactionMediums.map((m) => ({ id: m.id, label: m.name }))}
							placeholder="Medium"
							bind:value={editMediumId}
							onCreate={handleCreateInteractionMedium}
						/>
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
						entities={ltm.allTasks}
						linkedIds={ltm.linkedTaskIds}
						getDisplayName={ltm.taskName}
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
	.people-select {
		display: grid;
		gap: 0.35rem;
	}

	.org-names {
		font-size: 0.75rem;
		color: var(--text-secondary);
	}
</style>
