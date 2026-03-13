<script lang="ts">
	import { onMount } from 'svelte';
	import {
		api,
		type Organization,
		type OrgOrgRelationshipType,
		type OrgPersonRelationshipType,
		type Person,
		type PersonPersonRelationshipType,
		type RelationshipOrganizationOrganization,
		type RelationshipOrganizationPerson,
		type RelationshipPersonPerson
	} from '$lib';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';
	import { addToast } from '$lib/stores/toast';
	import { validateRequired } from '$lib/utils/validation';

	type TabId = 'person-person' | 'org-person' | 'org-org';
	let activeTab = $state<TabId>('person-person');

	const tabs: { id: TabId; label: string }[] = [
		{ id: 'person-person', label: 'Person \u2194 Person' },
		{ id: 'org-person', label: 'Org \u2192 Person' },
		{ id: 'org-org', label: 'Org \u2194 Org' }
	];

	let people: Person[] = $state([]);
	let organizations: Organization[] = $state([]);
	let personRelationships: RelationshipPersonPerson[] = $state([]);
	let orgRelationships: RelationshipOrganizationPerson[] = $state([]);
	let orgOrgRelationships: RelationshipOrganizationOrganization[] = $state([]);
	let ppRelTypes: PersonPersonRelationshipType[] = $state([]);
	let opRelTypes: OrgPersonRelationshipType[] = $state([]);
	let ooRelTypes: OrgOrgRelationshipType[] = $state([]);

	// Person-Person form state
	let newPerson1Id = $state<number | null>(null);
	let newPersonBIds = $state<number[]>([]);
	let newPersonTypeId = $state<number | null>(null);
	let newPersonNotes = $state('');
	let submittingPerson = $state(false);

	// Org-Person form state
	let newOrgId = $state<number | null>(null);
	let newOrgPersonIds = $state<number[]>([]);
	let newOrgTypeId = $state<number | null>(null);
	let newOrgNotes = $state('');
	let submittingOrg = $state(false);

	// Org-Org form state
	let newOrg1Id = $state<number | null>(null);
	let newOrgBIds = $state<number[]>([]);
	let newOrgOrgTypeId = $state<number | null>(null);
	let newOrgOrgNotes = $state('');
	let submittingOrgOrg = $state(false);

	function addPersonB(id: number): void {
		if (!newPersonBIds.includes(id)) newPersonBIds = [...newPersonBIds, id];
	}
	function removePersonB(id: number): void {
		newPersonBIds = newPersonBIds.filter((pid) => pid !== id);
	}
	function addOrgPerson(id: number): void {
		if (!newOrgPersonIds.includes(id)) newOrgPersonIds = [...newOrgPersonIds, id];
	}
	function removeOrgPerson(id: number): void {
		newOrgPersonIds = newOrgPersonIds.filter((pid) => pid !== id);
	}
	function addOrgB(id: number): void {
		if (!newOrgBIds.includes(id)) newOrgBIds = [...newOrgBIds, id];
	}
	function removeOrgB(id: number): void {
		newOrgBIds = newOrgBIds.filter((oid) => oid !== id);
	}

	// Filters
	let filterPersonId = $state<number | null>(null);
	let filterOrgId = $state<number | null>(null);
	let filterOrgOrgId = $state<number | null>(null);

	const filteredPersonRelationships = $derived(
		filterPersonId
			? personRelationships.filter(
					(r) => r.person_1_id === filterPersonId || r.person_2_id === filterPersonId
				)
			: personRelationships
	);

	const filteredOrgRelationships = $derived(
		filterOrgId
			? orgRelationships.filter((r) => r.organization_id === filterOrgId)
			: orgRelationships
	);

	const filteredOrgOrgRelationships = $derived(
		filterOrgOrgId
			? orgOrgRelationships.filter(
					(r) => r.org_1_id === filterOrgOrgId || r.org_2_id === filterOrgOrgId
				)
			: orgOrgRelationships
	);

	// Person-Person exclusions
	const connectedPersonIds = $derived(
		newPerson1Id
			? personRelationships
					.filter((r) => r.person_1_id === newPerson1Id || r.person_2_id === newPerson1Id)
					.map((r) => (r.person_1_id === newPerson1Id ? r.person_2_id : r.person_1_id))
			: []
	);

	const availablePersonBOptions = $derived(
		people
			.filter((p) => p.id !== newPerson1Id && !connectedPersonIds.includes(p.id) && !newPersonBIds.includes(p.id))
			.map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))
	);

	// Org-Person exclusions
	const connectedOrgPersonIds = $derived(
		newOrgId
			? orgRelationships.filter((r) => r.organization_id === newOrgId).map((r) => r.person_id)
			: []
	);

	const availableOrgPersonOptions = $derived(
		people
			.filter((p) => !connectedOrgPersonIds.includes(p.id) && !newOrgPersonIds.includes(p.id))
			.map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))
	);

	// Org-Org exclusions
	const connectedOrgIds = $derived(
		newOrg1Id
			? orgOrgRelationships
					.filter((r) => r.org_1_id === newOrg1Id || r.org_2_id === newOrg1Id)
					.map((r) => (r.org_1_id === newOrg1Id ? r.org_2_id : r.org_1_id))
			: []
	);

	const availableOrgBOptions = $derived(
		organizations
			.filter((o) => o.id !== newOrg1Id && !connectedOrgIds.includes(o.id) && !newOrgBIds.includes(o.id))
			.map((o) => ({ id: o.id, label: o.name }))
	);

	// Auto-sync filters from create form primary fields
	$effect(() => { filterPersonId = newPerson1Id; });
	$effect(() => { filterOrgId = newOrgId; });
	$effect(() => { filterOrgOrgId = newOrg1Id; });

	$effect(() => { if (newPersonBIds.length === 0) newPersonNotes = ''; });
	$effect(() => { if (newOrgPersonIds.length === 0) newOrgNotes = ''; });
	$effect(() => { if (newOrgBIds.length === 0) newOrgOrgNotes = ''; });

	// Inline editing
	let editingId = $state<number | null>(null);
	let editingType = $state<'person' | 'org' | 'org-org' | null>(null);
	let editingNotes = $state('');

	function startEdit(id: number, type: 'person' | 'org' | 'org-org', currentNotes: string): void {
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
		} else if (type === 'org') {
			const updated = await api.relationships.organizations.update(id, { notes });
			orgRelationships = orgRelationships.map((r) => (r.id === id ? updated : r));
		} else {
			const updated = await api.relationships.orgOrg.update(id, { notes });
			orgOrgRelationships = orgOrgRelationships.map((r) => (r.id === id ? updated : r));
		}
	}

	function handleEditKeydown(event: KeyboardEvent): void {
		if (event.key === 'Escape') cancelEdit();
	}

	function autofocus(node: HTMLTextAreaElement): void {
		node.focus();
	}

	// Relationship type creation helpers
	async function handleCreatePPRelType(name: string): Promise<{ id: number; label: string }> {
		const created = await api.relationshipTypes.people.create({ name });
		ppRelTypes = [...ppRelTypes, created].sort((a, b) => a.name.localeCompare(b.name));
		return { id: created.id, label: created.name };
	}

	async function handleCreateOPRelType(name: string): Promise<{ id: number; label: string }> {
		const created = await api.relationshipTypes.organizations.create({ name });
		opRelTypes = [...opRelTypes, created].sort((a, b) => a.name.localeCompare(b.name));
		return { id: created.id, label: created.name };
	}

	async function handleCreateOORelType(name: string): Promise<{ id: number; label: string }> {
		const created = await api.relationshipTypes.orgOrg.create({ name });
		ooRelTypes = [...ooRelTypes, created].sort((a, b) => a.name.localeCompare(b.name));
		return { id: created.id, label: created.name };
	}

	// Inline type updates
	async function updateRelType(relId: number, kind: 'person' | 'org' | 'org-org', typeId: number): Promise<void> {
		if (kind === 'person') {
			const updated = await api.relationships.people.update(relId, { relationship_type_id: typeId });
			personRelationships = personRelationships.map((r) => (r.id === relId ? updated : r));
		} else if (kind === 'org') {
			const updated = await api.relationships.organizations.update(relId, { relationship_type_id: typeId });
			orgRelationships = orgRelationships.map((r) => (r.id === relId ? updated : r));
		} else {
			const updated = await api.relationships.orgOrg.update(relId, { relationship_type_id: typeId });
			orgOrgRelationships = orgOrgRelationships.map((r) => (r.id === relId ? updated : r));
		}
	}

	// Data loading
	async function loadData(): Promise<void> {
		[people, organizations, personRelationships, orgRelationships, orgOrgRelationships, ppRelTypes, opRelTypes, ooRelTypes] =
			await Promise.all([
				api.people.getAll(),
				api.organizations.getAll(),
				api.relationships.people.getAll(),
				api.relationships.organizations.getAll(),
				api.relationships.orgOrg.getAll(),
				api.relationshipTypes.people.getAll(),
				api.relationshipTypes.organizations.getAll(),
				api.relationshipTypes.orgOrg.getAll()
			]);
	}

	onMount(() => { loadData(); });

	// Label helpers
	function personLabel(id: number): string {
		const person = people.find((item) => item.id === id);
		return person ? `${person.last_name}, ${person.first_name}` : 'Unknown';
	}

	function orgLabel(id: number): string {
		const org = organizations.find((item) => item.id === id);
		return org ? org.name : 'Unknown';
	}

	// CRUD: Person-Person
	async function createPersonRelationship(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!validateRequired({ 'Person A': newPerson1Id, 'Person B': newPersonBIds })) return;
		submittingPerson = true;
		const personAId = newPerson1Id!;
		const notes = newPersonNotes;
		const typeId = newPersonTypeId;
		const results = await Promise.allSettled(
			newPersonBIds.map((personBId) =>
				api.relationships.people.create({
					person_1_id: personAId,
					person_2_id: personBId,
					...(typeId ? { relationship_type_id: typeId } : {}),
					notes
				})
			)
		);
		const successIds: number[] = [];
		results.forEach((result, i) => {
			if (result.status === 'fulfilled') {
				personRelationships = [...personRelationships, result.value];
				successIds.push(newPersonBIds[i]);
			}
		});
		const failCount = results.filter((r) => r.status === 'rejected').length;
		if (failCount > 0) {
			addToast({ message: `${failCount} relationship${failCount !== 1 ? 's' : ''} failed to create`, type: 'error' });
		}
		newPersonBIds = newPersonBIds.filter((id) => !successIds.includes(id));
		if (newPersonBIds.length === 0) {
			newPerson1Id = null;
			newPersonTypeId = null;
			newPersonNotes = '';
		}
		submittingPerson = false;
	}

	// CRUD: Org-Person
	async function createOrgRelationship(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!validateRequired({ 'Organization': newOrgId, 'People': newOrgPersonIds })) return;
		submittingOrg = true;
		const orgId = newOrgId!;
		const notes = newOrgNotes;
		const typeId = newOrgTypeId;
		const results = await Promise.allSettled(
			newOrgPersonIds.map((personId) =>
				api.relationships.organizations.create({
					organization_id: orgId,
					person_id: personId,
					...(typeId ? { relationship_type_id: typeId } : {}),
					notes
				})
			)
		);
		const successIds: number[] = [];
		results.forEach((result, i) => {
			if (result.status === 'fulfilled') {
				orgRelationships = [...orgRelationships, result.value];
				successIds.push(newOrgPersonIds[i]);
			}
		});
		const failCount = results.filter((r) => r.status === 'rejected').length;
		if (failCount > 0) {
			addToast({ message: `${failCount} relationship${failCount !== 1 ? 's' : ''} failed to create`, type: 'error' });
		}
		newOrgPersonIds = newOrgPersonIds.filter((id) => !successIds.includes(id));
		if (newOrgPersonIds.length === 0) {
			newOrgId = null;
			newOrgTypeId = null;
			newOrgNotes = '';
		}
		submittingOrg = false;
	}

	// CRUD: Org-Org
	async function createOrgOrgRelationship(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!validateRequired({ 'Organization A': newOrg1Id, 'Organization B': newOrgBIds })) return;
		submittingOrgOrg = true;
		const orgAId = newOrg1Id!;
		const notes = newOrgOrgNotes;
		const typeId = newOrgOrgTypeId;
		const results = await Promise.allSettled(
			newOrgBIds.map((orgBId) =>
				api.relationships.orgOrg.create({
					org_1_id: orgAId,
					org_2_id: orgBId,
					...(typeId ? { relationship_type_id: typeId } : {}),
					notes
				})
			)
		);
		const successIds: number[] = [];
		results.forEach((result, i) => {
			if (result.status === 'fulfilled') {
				orgOrgRelationships = [...orgOrgRelationships, result.value];
				successIds.push(newOrgBIds[i]);
			}
		});
		const failCount = results.filter((r) => r.status === 'rejected').length;
		if (failCount > 0) {
			addToast({ message: `${failCount} relationship${failCount !== 1 ? 's' : ''} failed to create`, type: 'error' });
		}
		newOrgBIds = newOrgBIds.filter((id) => !successIds.includes(id));
		if (newOrgBIds.length === 0) {
			newOrg1Id = null;
			newOrgOrgTypeId = null;
			newOrgOrgNotes = '';
		}
		submittingOrgOrg = false;
	}

	// Delete functions
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

	async function deleteOrgOrgRelationship(id: number): Promise<void> {
		if (!confirm('Delete this relationship?')) return;
		await api.relationships.orgOrg.remove(id);
		orgOrgRelationships = orgOrgRelationships.filter((item) => item.id !== id);
	}

	function handleFormKeydown(e: KeyboardEvent): void {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			(e.currentTarget as HTMLElement).closest('form')?.requestSubmit();
		}
	}
</script>

<section class="relationships-page">
	<nav class="rel-tabs">
		{#each tabs as tab}
			<button class:active={activeTab === tab.id} onclick={() => (activeTab = tab.id)}>{tab.label}</button>
		{/each}
	</nav>

	<div class="tab-content">
		{#if activeTab === 'person-person'}
			<div class="panel">
				<h2>Person &#8596; Person</h2>
				<form class="create-form" onsubmit={createPersonRelationship}>
					<TypeaheadSelect
						options={people.map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))}
						placeholder="Person A"
						bind:value={newPerson1Id}
					/>
					<div class="people-select">
						<TypeaheadSelect
							options={availablePersonBOptions}
							placeholder="Add person..."
							onSelect={addPersonB}
						/>
						{#if newPersonBIds.length > 0}
							<div class="chips">
								{#each newPersonBIds as pid (pid)}
									<span class="chip">
										{personLabel(pid)}
										<button class="chip-remove" onclick={() => removePersonB(pid)}>&times;</button>
									</span>
								{/each}
							</div>
						{/if}
					</div>
					<TypeaheadSelect
						options={ppRelTypes.map((t) => ({ id: t.id, label: t.name }))}
						placeholder="Relationship type"
						bind:value={newPersonTypeId}
						onCreate={handleCreatePPRelType}
					/>
					<textarea bind:value={newPersonNotes} placeholder="Notes" onkeydown={handleFormKeydown}></textarea>
					<button type="submit" disabled={newPersonBIds.length === 0 || submittingPerson}>+ Add {newPersonBIds.length} Relationship{newPersonBIds.length !== 1 ? 's' : ''}</button>
				</form>

				<div class="filter-row">
					<TypeaheadSelect
						options={people.map((p) => ({ id: p.id, label: `${p.last_name}, ${p.first_name}` }))}
						placeholder="Filter by person"
						bind:value={filterPersonId}
					/>
					{#if filterPersonId}
						<button class="filter-clear" onclick={() => (filterPersonId = null)} title="Clear filter">&times;</button>
					{/if}
				</div>

				<div class="list">
					{#each filteredPersonRelationships as rel (rel.id)}
						<div class="list-item">
							<div class="title-row">
								<span class="title">{personLabel(rel.person_1_id)} &#8596; {personLabel(rel.person_2_id)}</span>
								{#if rel.relationship_type_name}
									<span class="type-label">{rel.relationship_type_name}</span>
								{/if}
							</div>
							<div class="type-select">
								<TypeaheadSelect
									options={ppRelTypes.map((t) => ({ id: t.id, label: t.name }))}
									placeholder="Set type"
									value={rel.relationship_type_id}
									onSelect={(id) => updateRelType(rel.id, 'person', id)}
									onCreate={handleCreatePPRelType}
								/>
							</div>
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
		{:else if activeTab === 'org-person'}
			<div class="panel">
				<h2>Organization &#8594; Person</h2>
				<form class="create-form" onsubmit={createOrgRelationship}>
					<TypeaheadSelect
						options={organizations.map((o) => ({ id: o.id, label: o.name }))}
						placeholder="Organization"
						bind:value={newOrgId}
					/>
					<div class="people-select">
						<TypeaheadSelect
							options={availableOrgPersonOptions}
							placeholder="Add person..."
							onSelect={addOrgPerson}
						/>
						{#if newOrgPersonIds.length > 0}
							<div class="chips">
								{#each newOrgPersonIds as pid (pid)}
									<span class="chip">
										{personLabel(pid)}
										<button class="chip-remove" onclick={() => removeOrgPerson(pid)}>&times;</button>
									</span>
								{/each}
							</div>
						{/if}
					</div>
					<TypeaheadSelect
						options={opRelTypes.map((t) => ({ id: t.id, label: t.name }))}
						placeholder="Role / type"
						bind:value={newOrgTypeId}
						onCreate={handleCreateOPRelType}
					/>
					<textarea bind:value={newOrgNotes} placeholder="Notes" onkeydown={handleFormKeydown}></textarea>
					<button type="submit" disabled={newOrgPersonIds.length === 0 || submittingOrg}>+ Add {newOrgPersonIds.length} Relationship{newOrgPersonIds.length !== 1 ? 's' : ''}</button>
				</form>

				<div class="filter-row">
					<TypeaheadSelect
						options={organizations.map((o) => ({ id: o.id, label: o.name }))}
						placeholder="Filter by organization"
						bind:value={filterOrgId}
					/>
					{#if filterOrgId}
						<button class="filter-clear" onclick={() => (filterOrgId = null)} title="Clear filter">&times;</button>
					{/if}
				</div>

				<div class="list">
					{#each filteredOrgRelationships as rel (rel.id)}
						<div class="list-item">
							<div class="title-row">
								<span class="title">{orgLabel(rel.organization_id)} &#8594; {personLabel(rel.person_id)}</span>
								{#if rel.relationship_type_name}
									<span class="type-label">{rel.relationship_type_name}</span>
								{/if}
							</div>
							<div class="type-select">
								<TypeaheadSelect
									options={opRelTypes.map((t) => ({ id: t.id, label: t.name }))}
									placeholder="Set role"
									value={rel.relationship_type_id}
									onSelect={(id) => updateRelType(rel.id, 'org', id)}
									onCreate={handleCreateOPRelType}
								/>
							</div>
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
		{:else}
			<div class="panel">
				<h2>Organization &#8596; Organization</h2>
				<form class="create-form" onsubmit={createOrgOrgRelationship}>
					<TypeaheadSelect
						options={organizations.map((o) => ({ id: o.id, label: o.name }))}
						placeholder="Organization A"
						bind:value={newOrg1Id}
					/>
					<div class="people-select">
						<TypeaheadSelect
							options={availableOrgBOptions}
							placeholder="Add organization..."
							onSelect={addOrgB}
						/>
						{#if newOrgBIds.length > 0}
							<div class="chips">
								{#each newOrgBIds as oid (oid)}
									<span class="chip">
										{orgLabel(oid)}
										<button class="chip-remove" onclick={() => removeOrgB(oid)}>&times;</button>
									</span>
								{/each}
							</div>
						{/if}
					</div>
					<TypeaheadSelect
						options={ooRelTypes.map((t) => ({ id: t.id, label: t.name }))}
						placeholder="Relationship type"
						bind:value={newOrgOrgTypeId}
						onCreate={handleCreateOORelType}
					/>
					<textarea bind:value={newOrgOrgNotes} placeholder="Notes" onkeydown={handleFormKeydown}></textarea>
					<button type="submit" disabled={newOrgBIds.length === 0 || submittingOrgOrg}>+ Add {newOrgBIds.length} Relationship{newOrgBIds.length !== 1 ? 's' : ''}</button>
				</form>

				<div class="filter-row">
					<TypeaheadSelect
						options={organizations.map((o) => ({ id: o.id, label: o.name }))}
						placeholder="Filter by organization"
						bind:value={filterOrgOrgId}
					/>
					{#if filterOrgOrgId}
						<button class="filter-clear" onclick={() => (filterOrgOrgId = null)} title="Clear filter">&times;</button>
					{/if}
				</div>

				<div class="list">
					{#each filteredOrgOrgRelationships as rel (rel.id)}
						<div class="list-item">
							<div class="title-row">
								<span class="title">{orgLabel(rel.org_1_id)} &#8596; {orgLabel(rel.org_2_id)}</span>
								{#if rel.relationship_type_name}
									<span class="type-label">{rel.relationship_type_name}</span>
								{/if}
							</div>
							<div class="type-select">
								<TypeaheadSelect
									options={ooRelTypes.map((t) => ({ id: t.id, label: t.name }))}
									placeholder="Set type"
									value={rel.relationship_type_id}
									onSelect={(id) => updateRelType(rel.id, 'org-org', id)}
									onCreate={handleCreateOORelType}
								/>
							</div>
							{#if editingId === rel.id && editingType === 'org-org'}
								<textarea
									class="edit-notes"
									bind:value={editingNotes}
									onblur={saveEdit}
									onkeydown={handleEditKeydown}
									use:autofocus
								></textarea>
							{:else}
								<button class="notes-btn" onclick={() => startEdit(rel.id, 'org-org', rel.notes || '')}>
									{#if rel.notes}
										<span class="meta">{rel.notes}</span>
									{:else}
										<span class="meta placeholder">&#9998; Add notes</span>
									{/if}
								</button>
							{/if}
							<div class="actions">
								<button class="danger" onclick={() => deleteOrgOrgRelationship(rel.id)}>Delete</button>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	</div>
</section>

<style>
	.relationships-page {
		display: grid;
		gap: 1rem;
		height: 100%;
		min-height: 0;
		grid-template-rows: auto 1fr;
	}

	h2 {
		margin: 0 0 0.5rem;
		font-family: var(--font-display);
		font-size: 1.1rem;
	}

	.rel-tabs {
		display: flex;
		gap: 0.25rem;
		background: var(--bg-surface-hover);
		border-radius: var(--radius-md);
		padding: 0.2rem;
		width: fit-content;
	}

	.rel-tabs button {
		all: unset;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--text-secondary);
		padding: 0.35rem 0.75rem;
		border-radius: var(--radius-sm);
		transition: all var(--transition);
	}

	.rel-tabs button:hover {
		color: var(--text-primary);
	}

	.rel-tabs button.active {
		background: var(--bg-surface);
		color: var(--text-primary);
		font-weight: 600;
		box-shadow: var(--shadow-sm);
	}

	.tab-content {
		min-height: 0;
		overflow-y: auto;
	}

	.panel {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.9rem;
		box-shadow: var(--shadow-sm);
		display: grid;
		gap: 0.75rem;
		align-content: start;
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

	.create-form button[type="submit"] {
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

	.create-form button[type="submit"]:hover {
		background: var(--accent);
		color: white;
		border-color: var(--accent);
	}

	.filter-row {
		display: flex;
		align-items: center;
		gap: 0.35rem;
		padding-top: 0.25rem;
		border-top: 1px solid var(--border-light, var(--border));
	}

	.filter-row :global(.typeahead) {
		flex: 1;
	}

	.filter-clear {
		all: unset;
		cursor: pointer;
		font-size: 1.1rem;
		line-height: 1;
		color: var(--text-tertiary);
		padding: 0.15rem 0.35rem;
		border-radius: var(--radius-sm);
		transition: color 0.15s, background 0.15s;
	}

	.filter-clear:hover {
		color: var(--error);
		background: var(--error-bg);
	}

	.people-select {
		display: grid;
		gap: 0.35rem;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.3rem;
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		background: var(--accent-light, var(--bg-surface-hover, #e8f0fe));
		border: 1px solid var(--border-light, var(--border));
		border-radius: var(--radius-sm);
		padding: 0.15rem 0.4rem;
		font-size: 0.75rem;
	}

	.chip-remove {
		all: unset;
		cursor: pointer;
		font-size: 0.85rem;
		line-height: 1;
		color: var(--text-tertiary);
		padding: 0 0.1rem;
	}

	.chip-remove:hover {
		color: var(--error, #dc3545);
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

	.title-row {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		flex-wrap: wrap;
	}

	.title {
		font-weight: 600;
		color: var(--text-primary);
	}

	.type-label {
		font-size: 0.7rem;
		padding: 0.1rem 0.35rem;
		background: var(--accent-light, var(--bg-surface-hover, #e8f0fe));
		border: 1px solid var(--border-light, var(--border));
		border-radius: var(--radius-sm);
		color: var(--text-secondary, var(--text-primary));
		white-space: nowrap;
	}

	.type-select {
		font-size: 0.85rem;
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

	@media (max-width: 640px) {
		.title {
			overflow: hidden;
			text-overflow: ellipsis;
			white-space: nowrap;
		}

		.actions button {
			min-height: 44px;
			padding: 0.35rem 0.65rem;
		}
	}
</style>
