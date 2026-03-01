<script lang="ts">
	import type { Task } from '$lib';
	import { api } from '$lib';
	import {
		timesheetStore,
		loadTimesheet,
		createTimeEntry,
		deleteTimeEntry
	} from '$lib/stores/timesheet';
	import { projectsStore, loadProjects } from '$lib/stores/projects';
	import { validateRequired } from '$lib/utils/validation';

	let weekOffset = $state(0);
	let newProjectId = $state<number | null>(null);
	let newDate = $state(today());
	let newDescription = $state('');
	let newTaskIds = $state<number[]>([]);
	let projectTasks = $state<Task[]>([]);

	function today(): string {
		const now = new Date();
		const y = now.getFullYear();
		const m = String(now.getMonth() + 1).padStart(2, '0');
		const d = String(now.getDate()).padStart(2, '0');
		return `${y}-${m}-${d}`;
	}

	function weekStartDate(offset: number): string {
		const d = new Date();
		d.setDate(d.getDate() - d.getDay() + offset * 7);
		const y = d.getFullYear();
		const m = String(d.getMonth() + 1).padStart(2, '0');
		const day = String(d.getDate()).padStart(2, '0');
		return `${y}-${m}-${day}`;
	}

	$effect(() => {
		loadTimesheet(weekStartDate(weekOffset));
		loadProjects();
	});

	$effect(() => {
		if (newProjectId !== null) {
			api.projects.getTasks(newProjectId).then((tasks) => {
				projectTasks = tasks;
			});
		} else {
			projectTasks = [];
		}
	});

	async function handleCreate(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!validateRequired({ 'Project': newProjectId })) return;
		await createTimeEntry({
			project_id: newProjectId!,
			date: newDate,
			description: newDescription.trim(),
			task_ids: newTaskIds
		});
		newDescription = '';
		newTaskIds = [];
	}

	async function handleDelete(entryId: number): Promise<void> {
		await deleteTimeEntry(entryId, weekStartDate(weekOffset));
	}

	function formatDate(dateStr: string): string {
		return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', {
			weekday: 'short',
			month: 'short',
			day: 'numeric'
		});
	}

	function formatTimeLocal(datetimeStr: string): string {
		return new Date(datetimeStr).toLocaleTimeString([], {
			hour: 'numeric',
			minute: '2-digit'
		});
	}

	interface FlatTask {
		id: number;
		title: string;
		depth: number;
	}

	function flattenTaskTree(tasks: Task[], depth = 0): FlatTask[] {
		const result: FlatTask[] = [];
		for (const task of tasks) {
			result.push({ id: task.id, title: task.title, depth: Math.min(depth, 3) });
			if (task.subtasks?.length) {
				result.push(...flattenTaskTree(task.subtasks, depth + 1));
			}
		}
		return result;
	}

	let flatTasks = $derived(flattenTaskTree(projectTasks.filter((t) => !t.parent_id)));

	function toggleTask(taskId: number): void {
		if (newTaskIds.includes(taskId)) {
			newTaskIds = newTaskIds.filter((id) => id !== taskId);
		} else {
			newTaskIds = [...newTaskIds, taskId];
		}
	}

	function formatTaskBreadcrumb(detail: {
		title: string;
		parent_titles: string[];
	}): string {
		if (detail.parent_titles.length === 0) return detail.title;
		const parent = detail.parent_titles[detail.parent_titles.length - 1];
		return `${parent} \u203a ${detail.title}`;
	}

	function formatEntryTasks(
		details: Array<{ id: number; title: string; parent_titles: string[] }>
	): string {
		const MAX_DISPLAY = 3;
		const displayed = details.slice(0, MAX_DISPLAY).map(formatTaskBreadcrumb);
		const remaining = details.length - MAX_DISPLAY;
		if (remaining > 0) {
			return displayed.join(', ') + `, +${remaining} more`;
		}
		return displayed.join(', ');
	}
</script>

<section class="timesheet-page">
	<header>
		<h1>Timesheet</h1>
		<div class="week-nav">
			<button onclick={() => weekOffset--}>&larr; Prev</button>
			<span class="week-label">
				{#if $timesheetStore}
					{formatDate($timesheetStore.week_start)} &mdash; {formatDate($timesheetStore.week_end)}
				{/if}
			</span>
			<button onclick={() => weekOffset++}>Next &rarr;</button>
		</div>
	</header>

	{#if $timesheetStore}
		<div class="summary-bar">
			<span class="total">Total: {$timesheetStore.summary.total_hours}h ({$timesheetStore.summary.overall_total_hours}h total)</span>
			{#each $timesheetStore.summary.per_project as item}
				<span class="project-hours">{item.project_name}: {item.hours}h ({item.overall_hours}h total)</span>
			{/each}
		</div>

		<form class="entry-form" onsubmit={handleCreate}>
			<select bind:value={newProjectId}>
				<option value={null}>Select project...</option>
				{#each $projectsStore as project}
					<option value={project.id}>{project.name}</option>
				{/each}
			</select>
			<input type="date" bind:value={newDate} />
			<input bind:value={newDescription} placeholder="Description..." />
			{#if flatTasks.length > 0}
				<div class="task-picker">
					{#each flatTasks as task}
						<label
							class="task-row"
							class:subtask={task.depth > 0}
							style="padding-left: {0.5 + task.depth * 1.25}rem"
						>
							<input
								type="checkbox"
								checked={newTaskIds.includes(task.id)}
								onchange={() => toggleTask(task.id)}
							/>
							<span class="task-title">{task.title}</span>
						</label>
					{/each}
				</div>
			{/if}
			<button type="submit">+ Entry</button>
		</form>

		<div class="entries">
			{#each Object.entries($timesheetStore.entries_by_date) as [date, entries]}
				<div class="date-group">
					<h3>{formatDate(date)}</h3>
					{#each entries as entry}
						<div class="entry-row">
							<span class="entry-project">{entry.project_name}</span>
							<span class="entry-time">{formatTimeLocal(entry.created_at)}</span>
							{#if entry.description}
								<span class="entry-desc">{entry.description}</span>
							{/if}
							{#if entry.task_details?.length}
								<span class="entry-tasks">{formatEntryTasks(entry.task_details)}</span>
							{/if}
							<button class="delete-btn" onclick={() => handleDelete(entry.id)}>&#10005;</button>
						</div>
					{/each}
				</div>
			{/each}
		</div>
	{/if}
</section>

<style>
	.timesheet-page {
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

	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.week-nav {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.week-nav button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.3rem 0.6rem;
		cursor: pointer;
		font-size: 0.78rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.week-nav button:hover {
		background: var(--bg-surface-hover);
		border-color: var(--accent);
		color: var(--accent);
	}

	.week-label {
		font-weight: 600;
		font-size: 0.88rem;
		color: var(--text-primary);
	}

	.summary-bar {
		display: flex;
		gap: 1rem;
		padding: 0.65rem 0.85rem;
		background: var(--accent-light);
		border: 1px solid var(--accent-medium);
		border-radius: var(--radius-md);
		font-size: 0.85rem;
	}

	.total {
		font-weight: 700;
		color: var(--accent);
	}

	.project-hours {
		color: var(--text-secondary);
	}

	.entry-form {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem;
		align-items: flex-start;
	}

	.entry-form select,
	.entry-form input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.5rem;
		font-size: 0.85rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		background: var(--bg-input);
	}

	.entry-form select:focus,
	.entry-form input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.task-picker {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--bg-input);
		max-height: 12rem;
		overflow-y: auto;
		width: 100%;
	}

	.task-row {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0.25rem 0.5rem;
		cursor: pointer;
		font-size: 0.85rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		transition: background var(--transition);
	}

	.task-row:hover {
		background: var(--bg-surface-hover);
	}

	.task-row.subtask .task-title {
		color: var(--text-secondary);
		font-size: 0.82rem;
	}

	.task-row input[type='checkbox'] {
		flex-shrink: 0;
	}

	.entry-form button {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.7rem;
		cursor: pointer;
		font-family: var(--font-body);
		font-size: 0.82rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.entry-form button:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}

	.entries {
		display: grid;
		gap: 0.75rem;
	}

	.date-group h3 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 0.9rem;
		font-weight: 600;
		color: var(--text-secondary);
		border-bottom: 1px solid var(--border-light);
		padding-bottom: 0.35rem;
	}

	.entry-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.35rem 0.45rem;
		border-radius: var(--radius-sm);
		transition: background var(--transition);
	}

	.entry-row:hover {
		background: var(--bg-surface-hover);
	}

	.entry-project {
		font-weight: 600;
		font-size: 0.85rem;
		color: var(--text-primary);
	}

	.entry-time {
		font-size: 0.78rem;
		color: var(--text-tertiary);
	}

	.entry-desc {
		color: var(--text-secondary);
		font-size: 0.85rem;
		flex: 1;
	}

	.entry-tasks {
		color: var(--text-secondary);
		font-size: 0.8rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		max-width: 20rem;
	}

	.delete-btn {
		background: transparent;
		border: none;
		cursor: pointer;
		color: var(--error);
		opacity: 0;
		transition: opacity var(--transition);
	}

	.entry-row:hover .delete-btn {
		opacity: 1;
	}

	@media (max-width: 640px) {
		.summary-bar {
			flex-wrap: wrap;
		}

		.entry-form {
			flex-direction: column;
		}

		.entry-form select,
		.entry-form input,
		.entry-form button,
		.task-picker {
			width: 100%;
		}

		.entry-tasks {
			white-space: normal;
			max-width: none;
		}

		.week-nav {
			flex-wrap: wrap;
			justify-content: center;
		}

		.week-label {
			font-size: 0.8rem;
			text-align: center;
		}

		.entry-row {
			flex-wrap: wrap;
		}

		.delete-btn {
			opacity: 1;
		}
	}
</style>
