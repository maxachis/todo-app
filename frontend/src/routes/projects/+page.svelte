<script lang="ts">
	import {
		projectsStore,
		loadProjects,
		createProject,
		updateProject,
		toggleProject,
		deleteProject,
		createProjectLink,
		deleteProjectLink
	} from '$lib/stores/projects';
	import NotebookMentions from '$lib/components/shared/NotebookMentions.svelte';

	let newName = $state('');
	let newDescription = $state('');
	let editingId = $state<number | null>(null);
	let editName = $state('');
	let editDescription = $state('');
	let addingLinkProjectId = $state<number | null>(null);
	let newLinkDescriptor = $state('');
	let newLinkUrl = $state('');

	$effect(() => {
		loadProjects();
	});

	async function handleCreate(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newName.trim()) return;
		await createProject({ name: newName.trim(), description: newDescription.trim() });
		newName = '';
		newDescription = '';
	}

	function startEdit(project: { id: number; name: string; description: string }): void {
		editingId = project.id;
		editName = project.name;
		editDescription = project.description;
	}

	async function commitEdit(): Promise<void> {
		if (editingId === null || !editName.trim()) return;
		await updateProject(editingId, { name: editName.trim(), description: editDescription.trim() });
		editingId = null;
	}

	async function handleDelete(id: number): Promise<void> {
		if (!confirm('Delete this project? Lists will be unlinked, not deleted.')) return;
		await deleteProject(id);
	}

	async function handleAddLink(projectId: number, event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!newLinkDescriptor.trim() || !newLinkUrl.trim()) return;
		await createProjectLink(projectId, {
			descriptor: newLinkDescriptor.trim(),
			url: newLinkUrl.trim()
		});
		newLinkDescriptor = '';
		newLinkUrl = '';
		addingLinkProjectId = null;
	}

	async function handleDeleteLink(projectId: number, linkId: number): Promise<void> {
		await deleteProjectLink(projectId, linkId);
	}
</script>

<section class="projects-page">
	<header>
		<h1>Projects</h1>
	</header>

	<form class="create-form" onsubmit={handleCreate}>
		<input bind:value={newName} placeholder="Project name..." />
		<input bind:value={newDescription} placeholder="Description (optional)" />
		<button type="submit">+ Project</button>
	</form>

	<div class="projects-grid">
		{#each $projectsStore as project (project.id)}
			<div class="project-card" class:inactive={!project.is_active}>
				{#if editingId === project.id}
					<input class="edit-input" bind:value={editName} onkeydown={(e) => { if (e.key === 'Enter') commitEdit(); if (e.key === 'Escape') editingId = null; }} />
					<input class="edit-input" bind:value={editDescription} placeholder="Description" />
					<div class="card-actions">
						<button onclick={commitEdit}>Save</button>
						<button onclick={() => (editingId = null)}>Cancel</button>
					</div>
				{:else}
					<h3>{project.name}</h3>
					{#if project.description}
						<p class="description">{project.description}</p>
					{/if}
					{#if project.links && project.links.length > 0}
						<div class="project-links">
							{#each project.links as link (link.id)}
								<div class="link-row">
									<a href={link.url} target="_blank" rel="noopener noreferrer">{link.descriptor}</a>
									<button class="link-delete-btn" onclick={() => handleDeleteLink(project.id, link.id)}>&times;</button>
								</div>
							{/each}
						</div>
					{/if}
					{#if addingLinkProjectId === project.id}
						<form class="add-link-form" onsubmit={(e) => handleAddLink(project.id, e)}>
							<input bind:value={newLinkDescriptor} placeholder="Label (e.g. GitHub)" />
							<input bind:value={newLinkUrl} placeholder="URL" />
							<button type="submit">Add</button>
							<button type="button" onclick={() => (addingLinkProjectId = null)}>Cancel</button>
						</form>
					{:else}
						<button class="add-link-btn" onclick={() => { addingLinkProjectId = project.id; newLinkDescriptor = ''; newLinkUrl = ''; }}>+ Link</button>
					{/if}
					<div class="metrics">
						<span>📊 {project.total_hours ?? 0}h logged</span>
						<span>📋 {project.linked_lists_count ?? 0} lists</span>
						<span>✅ {project.completed_tasks ?? 0}/{project.total_tasks ?? 0} tasks</span>
					</div>
					<div class="card-actions">
						<button class="toggle-btn" onclick={() => toggleProject(project.id)}>
							{project.is_active ? '🟢 Active' : '⚪ Inactive'}
						</button>
						<button onclick={() => startEdit(project)}>Edit</button>
						<button class="delete-btn" onclick={() => handleDelete(project.id)}>Delete</button>
					</div>
					<NotebookMentions entityType="project" entityId={project.id} />
				{/if}
			</div>
		{/each}
	</div>

	{#if $projectsStore.length === 0}
		<div class="empty-state">
			<p>No projects yet. Create one to get started.</p>
		</div>
	{/if}
</section>

<style>
	.projects-page {
		display: grid;
		gap: 1rem;
	}

	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.create-form {
		display: grid;
		grid-template-columns: 1fr 1fr auto;
		gap: 0.35rem;
	}

	.create-form input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.4rem 0.6rem;
		font-family: var(--font-body);
		font-size: 0.85rem;
		color: var(--text-primary);
		background: var(--bg-input);
	}

	.create-form input::placeholder {
		color: var(--text-tertiary);
	}

	.create-form input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.create-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.75rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.82rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.create-form button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.projects-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 0.85rem;
	}

	.project-card {
		background: var(--bg-surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: 0.95rem;
		display: grid;
		gap: 0.55rem;
		box-shadow: var(--shadow-sm);
		transition: box-shadow var(--transition);
	}

	.project-card:hover {
		box-shadow: var(--shadow-md);
	}

	.project-card.inactive {
		opacity: 0.55;
	}

	h3 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 1.05rem;
		font-weight: 600;
		color: var(--text-primary);
	}

	.description {
		margin: 0;
		color: var(--text-secondary);
		font-size: 0.85rem;
		line-height: 1.5;
	}

	.metrics {
		display: flex;
		gap: 0.75rem;
		font-size: 0.76rem;
		color: var(--text-tertiary);
	}

	.card-actions {
		display: flex;
		gap: 0.35rem;
	}

	.card-actions button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.5rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.card-actions button:hover {
		background: var(--bg-surface-hover);
		border-color: var(--accent);
		color: var(--accent);
	}

	.delete-btn {
		color: var(--error) !important;
	}

	.delete-btn:hover {
		border-color: var(--error) !important;
		background: var(--error-bg) !important;
	}

	.project-links {
		display: grid;
		gap: 0.2rem;
	}

	.link-row {
		display: flex;
		align-items: center;
		gap: 0.35rem;
	}

	.link-row a {
		font-size: 0.82rem;
		color: var(--accent);
		text-decoration: none;
	}

	.link-row a:hover {
		text-decoration: underline;
	}

	.link-delete-btn {
		border: none;
		background: none;
		cursor: pointer;
		font-size: 0.85rem;
		color: var(--text-tertiary);
		padding: 0 0.15rem;
		line-height: 1;
	}

	.link-delete-btn:hover {
		color: var(--error);
	}

	.add-link-btn {
		border: 1px dashed var(--border);
		background: none;
		border-radius: var(--radius-sm);
		padding: 0.2rem 0.5rem;
		cursor: pointer;
		font-size: 0.76rem;
		font-family: var(--font-body);
		color: var(--text-tertiary);
		justify-self: start;
		transition: all var(--transition);
	}

	.add-link-btn:hover {
		border-color: var(--accent);
		color: var(--accent);
	}

	.add-link-form {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.25rem;
	}

	.add-link-form input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.4rem;
		font-size: 0.8rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		background: var(--bg-input);
		min-width: 0;
	}

	.add-link-form input::placeholder {
		color: var(--text-tertiary);
	}

	.add-link-form input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.add-link-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.2rem 0.45rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.add-link-form button:hover {
		background: var(--bg-surface-hover);
	}

	.edit-input {
		border: 1px solid var(--border-focus);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.5rem;
		font-size: 0.88rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		background: var(--bg-input);
	}

	.edit-input:focus {
		outline: none;
	}

	.empty-state {
		border: 2px dashed var(--border);
		border-radius: var(--radius-lg);
		min-height: 120px;
		display: grid;
		place-items: center;
		background: var(--bg-surface-hover);
	}

	.empty-state p {
		color: var(--text-secondary);
		font-weight: 500;
	}

	@media (max-width: 640px) {
		.create-form {
			grid-template-columns: 1fr;
		}

		.card-actions button {
			min-height: 44px;
			padding: 0.35rem 0.65rem;
		}

		.metrics {
			flex-wrap: wrap;
		}
	}
</style>
