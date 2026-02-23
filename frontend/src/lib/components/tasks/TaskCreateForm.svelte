<script lang="ts">
	import * as chrono from 'chrono-node';
	import { createTask } from '$lib/stores/tasks';

	let {
		sectionId,
		parentId = null
	}: {
		sectionId: number;
		parentId?: number | null;
	} = $props();

	let title = $state('');
	let dueDate = $state('');

	let detecting = $state(true);
	let settingProgrammatically = false;

	function formatDateForPicker(date: Date): string {
		const y = date.getFullYear();
		const m = String(date.getMonth() + 1).padStart(2, '0');
		const d = String(date.getDate()).padStart(2, '0');
		return `${y}-${m}-${d}`;
	}

	function handleTitleInput(): void {
		if (!detecting) return;

		const parsed = chrono.parseDate(title);
		if (parsed) {
			settingProgrammatically = true;
			dueDate = formatDateForPicker(parsed);
			settingProgrammatically = false;
		}
		// If no date found, current picker value sticks
	}

	function handleDatePickerChange(): void {
		if (settingProgrammatically) return;
		// User manually interacted with picker — stop detecting
		detecting = false;
	}

	async function submit(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		const trimmed = title.trim();
		if (!trimmed) return;
		await createTask(sectionId, {
			title: trimmed,
			...(parentId !== null ? { parent_id: parentId } : {}),
			...(dueDate ? { due_date: dueDate } : {})
		});
		title = '';
		dueDate = '';
		detecting = true;
	}
</script>

<form class="create-form" data-section-id={sectionId} onsubmit={submit}>
	<input
		bind:value={title}
		oninput={handleTitleInput}
		placeholder={parentId !== null ? 'Add subtask...' : 'Add task...'}
		class="task-input"
	/>
	<input
		type="date"
		bind:value={dueDate}
		onchange={handleDatePickerChange}
		class="date-input"
		title="Due date"
	/>
	<button type="submit" class="add-btn">+</button>
</form>

<style>
	.create-form {
		display: grid;
		grid-template-columns: 1fr auto auto;
		gap: 0.3rem;
		padding: 0.25rem 0;
	}

	.task-input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.55rem;
		font-size: 0.85rem;
		font-family: var(--font-body);
		color: var(--text-primary);
		background: var(--bg-input);
		transition: border-color var(--transition);
	}

	.task-input::placeholder {
		color: var(--text-tertiary);
	}

	.task-input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	.date-input {
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		padding: 0.35rem 0.4rem;
		font-size: 0.8rem;
		font-family: var(--font-body);
		color: var(--text-secondary);
		background: var(--bg-input);
		transition: border-color var(--transition);
		max-width: 8.5rem;
	}

	.date-input:focus {
		outline: none;
		border-color: var(--border-focus);
	}

	@media (max-width: 480px) {
		.date-input {
			max-width: 7rem;
			padding: 0.35rem 0.25rem;
			font-size: 0.75rem;
		}
	}

	.add-btn {
		border: 1px solid var(--border);
		background: var(--bg-surface);
		border-radius: var(--radius-sm);
		padding: 0.25rem 0.6rem;
		cursor: pointer;
		font-size: 1rem;
		color: var(--text-secondary);
		transition: all var(--transition);
	}

	.add-btn:hover {
		background: var(--accent);
		border-color: var(--accent);
		color: white;
	}
</style>
