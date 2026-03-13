<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Lead, type Person, type Organization } from '$lib';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';
	import { createLinkedTasksManager } from '$lib/components/shared/linkedTasks.svelte';
	import { validateRequired } from '$lib/utils/validation';
	import { addToast } from '$lib/stores/toast';

	const ltm = createLinkedTasksManager('leads');

	let leads: Lead[] = $state([]);
	let selected: Lead | null = $state(null);
	let people: Person[] = $state([]);
	let organizations: Organization[] = $state([]);

	const statusOptions = [
		{ value: 'prospect', label: 'Prospect' },
		{ value: 'interested', label: 'Interested' },
		{ value: 'committed', label: 'Committed' },
		{ value: 'fulfilled', label: 'Fulfilled' },
		{ value: 'unfulfilled', label: 'Unfulfilled' }
	];

	// Create form state
	let newTitle = $state('');
	let newNotes = $state('');
	let newPersonId = $state<number | null>(null);
	let newOrgId = $state<number | null>(null);

	// Edit form state
	let editTitle = $state('');
	let editStatus = $state('prospect');
	let editNotes = $state('');
	let editPersonId = $state<number | null>(null);
	let editOrgId = $state<number | null>(null);

	async function loadLeads(): Promise<void> {
		leads = await api.leads.getAll();
		if (selected) {
			selected = leads.find((l) => l.id === selected?.id) ?? null;
		}
	}

	onMount(() => {
		loadLeads();
		api.people.getAll().then((p) => (people = p));
		api.organizations.getAll().then((o) => (organizations = o));
	});

	function selectLead(lead: Lead): void {
		selected = lead;
		editTitle = lead.title;
		editStatus = lead.status;
		editNotes = lead.notes;
		editPersonId = lead.person_id;
		editOrgId = lead.organization_id;
		ltm.loadLinkedTasks(lead.id);
	}

	async function addTaskLink(taskId: number): Promise<void> {
		if (selected) ltm.addTaskLink(selected.id, taskId);
	}

	async function removeTaskLink(taskId: number): Promise<void> {
		if (selected) ltm.removeTaskLink(selected.id, taskId);
	}

	function contactLabel(lead: Lead): string {
		const parts: string[] = [];
		if (lead.person_name) parts.push(lead.person_name);
		if (lead.organization_name) parts.push(lead.organization_name);
		return parts.join(' · ');
	}

	async function createLead(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!validateRequired({ 'Title': newTitle })) return;
		if (!newPersonId && !newOrgId) {
			addToast({ message: 'Required: Person or Organization', type: 'error' });
			return;
		}
		const lead = await api.leads.create({
			title: newTitle.trim(),
			notes: newNotes,
			person_id: newPersonId,
			organization_id: newOrgId
		});
		leads = [lead, ...leads];
		newTitle = '';
		newNotes = '';
		newPersonId = null;
		newOrgId = null;
	}

	async function selectPerson(personId: number): Promise<void> {
		editPersonId = personId;
		await saveLead();
	}

	async function selectOrganization(orgId: number): Promise<void> {
		editOrgId = orgId;
		await saveLead();
	}

	async function saveLead(): Promise<void> {
		if (!selected) return;
		const updated = await api.leads.update(selected.id, {
			title: editTitle.trim(),
			status: editStatus,
			notes: editNotes,
			person_id: editPersonId,
			organization_id: editOrgId
		});
		leads = leads.map((l) => (l.id === updated.id ? updated : l));
		selected = updated;
	}

	async function deleteLead(lead: Lead): Promise<void> {
		if (!confirm(`Delete "${lead.title}"?`)) return;
		await api.leads.remove(lead.id);
		leads = leads.filter((l) => l.id !== lead.id);
		if (selected?.id === lead.id) {
			selected = null;
		}
	}
</script>

<section class="crm-page">
	<header>
		<h1>Leads</h1>
	</header>

	<div class="crm-grid">
		<div class="panel list-panel">
			<form class="create-form" onsubmit={createLead}>
				<input bind:value={newTitle} placeholder="Lead title" />
				<TypeaheadSelect
					options={people.map((p) => ({ id: p.id, label: `${p.first_name} ${p.last_name}` }))}
					placeholder="Person (optional)"
					bind:value={newPersonId}
				/>
				<TypeaheadSelect
					options={organizations.map((o) => ({ id: o.id, label: o.name }))}
					placeholder="Organization (optional)"
					bind:value={newOrgId}
				/>
				<textarea rows="2" bind:value={newNotes} placeholder="Notes (optional)"></textarea>
				<button type="submit">+ Lead</button>
			</form>

			<div class="list">
				{#each leads as lead (lead.id)}
					<button class="list-item" class:active={selected?.id === lead.id} onclick={() => selectLead(lead)}>
						<div class="list-item-row">
							<div class="list-item-content">
								<div class="title">{lead.title}</div>
								{#if contactLabel(lead)}
									<div class="contact">{contactLabel(lead)}</div>
								{/if}
							</div>
							<span class="status-badge status-{lead.status}">{lead.status}</span>
						</div>
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{selected.title}</h2>
					<button class="danger" onclick={() => selected && deleteLead(selected)}>Delete</button>
				</div>

				<div class="detail-form">
					<label>
						<span>Title</span>
						<input bind:value={editTitle} onblur={saveLead} />
					</label>
					<label>
						<span>Status</span>
						<select bind:value={editStatus} onchange={saveLead}>
							{#each statusOptions as opt}
								<option value={opt.value}>{opt.label}</option>
							{/each}
						</select>
					</label>
					<div class="typeahead-field">
						<span class="field-label">Person</span>
						<TypeaheadSelect
							options={people.map((p) => ({ id: p.id, label: `${p.first_name} ${p.last_name}` }))}
							placeholder="Select person"
							onSelect={selectPerson}
						/>
					</div>
					<div class="typeahead-field">
						<span class="field-label">Organization</span>
						<TypeaheadSelect
							options={organizations.map((o) => ({ id: o.id, label: o.name }))}
							placeholder="Select organization"
							onSelect={selectOrganization}
						/>
					</div>
					<label>
						<span>Notes</span>
						<textarea rows="5" bind:value={editNotes} onblur={saveLead}></textarea>
					</label>
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
				<div class="empty-state">Select a lead to view details.</div>
			{/if}
		</div>
	</div>
</section>

<style>
	.list-item {
		width: 100%;
	}

	.list-item-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
	}

	.list-item-content {
		min-width: 0;
	}

	.contact {
		font-size: 0.78rem;
		color: var(--text-secondary);
		margin-top: 0.15rem;
	}

	.status-badge {
		font-size: 0.7rem;
		font-weight: 600;
		padding: 0.15rem 0.4rem;
		border-radius: var(--radius-sm);
		white-space: nowrap;
		flex-shrink: 0;
		text-transform: capitalize;
	}

	.status-prospect {
		background: rgba(100, 140, 200, 0.12);
		color: #4a6fa5;
		border: 1px solid rgba(100, 140, 200, 0.3);
	}

	.status-interested {
		background: rgba(200, 155, 60, 0.1);
		color: #8a6914;
		border: 1px solid rgba(200, 155, 60, 0.3);
	}

	:global(:root[data-theme='dark']) .status-interested {
		color: #c9a84c;
	}

	.status-committed {
		background: var(--success-bg);
		color: var(--success);
		border: 1px solid var(--success-border);
	}

	.status-fulfilled {
		background: var(--success-bg);
		color: var(--success);
		border: 1px solid var(--success-border);
	}

	.status-unfulfilled {
		background: var(--error-bg);
		color: var(--error);
		border: 1px solid var(--error-border);
	}

	:global(:root[data-theme='dark']) .status-prospect {
		color: #7da3d4;
	}

	.typeahead-field {
		display: grid;
		gap: 0.25rem;
	}
</style>
