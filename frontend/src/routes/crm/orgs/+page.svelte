<script lang="ts">
	import { onMount } from 'svelte';
	import { api, type Organization, type OrgType } from '$lib';
	import { ApiError } from '$lib/api/client';
	import { addToast } from '$lib/stores/toast';
	import { validateRequired } from '$lib/utils/validation';
	import LinkedEntities from '$lib/components/shared/LinkedEntities.svelte';
	import TypeaheadSelect from '$lib/components/shared/TypeaheadSelect.svelte';
	import { createLinkedTasksManager } from '$lib/components/shared/linkedTasks.svelte';
	import NotebookMentions from '$lib/components/shared/NotebookMentions.svelte';

	const ltm = createLinkedTasksManager('organizations');

	let organizations: Organization[] = $state([]);
	let orgTypes: OrgType[] = $state([]);
	let selected: Organization | null = $state(null);

	let filterQuery = $state('');

	let filteredOrganizations: Organization[] = $derived.by(() => {
		const q = filterQuery.trim().toLowerCase();
		return q
			? organizations.filter(o => o.name.toLowerCase().includes(q))
			: organizations;
	});

	let newOrgName = $state('');
	let newOrgNotes = $state('');
	let newOrgTypeId = $state<number | null>(null);

	let editName = $state('');
	let editNotes = $state('');
	let editOrgTypeId = $state<number | null>(null);

	async function loadData(): Promise<void> {
		orgTypes = await api.orgTypes.getAll();
		organizations = await api.organizations.getAll();
		if (selected) {
			selected = organizations.find((org) => org.id === selected?.id) ?? null;
		}
	}

	onMount(() => {
		loadData();
	});

	function selectOrg(org: Organization): void {
		selected = org;
		editName = org.name;
		editNotes = org.notes;
		editOrgTypeId = org.org_type_id;
		ltm.loadLinkedTasks(org.id);
	}

	async function addTaskLink(taskId: number): Promise<void> {
		if (selected) ltm.addTaskLink(selected.id, taskId);
	}

	async function removeTaskLink(taskId: number): Promise<void> {
		if (selected) ltm.removeTaskLink(selected.id, taskId);
	}

	async function handleCreateOrgType(name: string): Promise<{ id: number; label: string }> {
		const created = await api.orgTypes.create({ name });
		orgTypes = [...orgTypes, created].sort((a, b) => a.name.localeCompare(b.name));
		return { id: created.id, label: created.name };
	}

	async function createOrganization(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!validateRequired({ 'Name': newOrgName, 'Organization type': newOrgTypeId })) return;
		try {
			const created = await api.organizations.create({
				name: newOrgName.trim(),
				org_type_id: newOrgTypeId!,
				notes: newOrgNotes.trim()
			});
			organizations = [...organizations, created].sort((a, b) => a.name.localeCompare(b.name));
			newOrgName = '';
			newOrgNotes = '';
		} catch (err) {
			if (err instanceof ApiError && err.status === 409) {
				const detail = (err.body as { detail?: string })?.detail ?? 'An organization with that name already exists.';
				addToast({ message: detail, type: 'error' });
				return;
			}
			throw err;
		}
	}

	async function saveOrganization(): Promise<void> {
		if (!selected || !editOrgTypeId) return;
		const updated = await api.organizations.update(selected.id, {
			name: editName.trim(),
			org_type_id: editOrgTypeId,
			notes: editNotes
		});
		organizations = organizations.map((org) => (org.id === updated.id ? updated : org));
		selected = updated;
	}

	async function deleteOrganization(org: Organization): Promise<void> {
		if (!confirm(`Delete ${org.name}?`)) return;
		await api.organizations.remove(org.id);
		organizations = organizations.filter((item) => item.id !== org.id);
		if (selected?.id === org.id) {
			selected = null;
		}
	}
</script>

<section class="crm-page">
	<header>
		<h1>Organizations</h1>
	</header>

	<div class="crm-grid">
		<div class="panel list-panel">
			<form class="create-form" onsubmit={createOrganization}>
				<input bind:value={newOrgName} placeholder="Organization name" />
				<TypeaheadSelect
					options={orgTypes.map((t) => ({ id: t.id, label: t.name }))}
					placeholder="Org type"
					bind:value={newOrgTypeId}
					onCreate={handleCreateOrgType}
				/>
				<textarea bind:value={newOrgNotes} placeholder="Notes"></textarea>
				<button type="submit">+ Organization</button>
			</form>

			<input class="filter-input" type="text" placeholder="Filter by name…" bind:value={filterQuery} />

			<div class="list">
				{#each filteredOrganizations as org (org.id)}
					<button class="list-item" class:active={selected?.id === org.id} onclick={() => selectOrg(org)}>
						<div class="title">{org.name}</div>
						<div class="meta">{orgTypes.find((type) => type.id === org.org_type_id)?.name ?? '—'}</div>
					</button>
				{/each}
			</div>
		</div>

		<div class="panel detail-panel">
			{#if selected}
				<div class="detail-header">
					<h2>{selected.name}</h2>
					<button class="danger" onclick={() => selected && deleteOrganization(selected)}>Delete</button>
				</div>
				<div class="detail-form">
					<label>
						<span>Name</span>
						<input bind:value={editName} />
					</label>
					<label>
						<span>Org type</span>
						<TypeaheadSelect
							options={orgTypes.map((t) => ({ id: t.id, label: t.name }))}
							placeholder="Org type"
							bind:value={editOrgTypeId}
							onCreate={handleCreateOrgType}
						/>
					</label>
					<label>
						<span>Notes</span>
						<textarea rows="5" bind:value={editNotes}></textarea>
					</label>
					<button class="primary" onclick={saveOrganization}>Save</button>
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
				<NotebookMentions entityType="organization" entityId={selected.id} />
			{:else}
				<div class="empty-state">Select an organization to view details.</div>
			{/if}
		</div>
	</div>
</section>

<style>
	/* All styles provided by crm.css via the CRM layout */
</style>
