<script lang="ts">
	import * as chrono from 'chrono-node';
	import { createTask, selectTask } from '$lib/stores/tasks';
	import { validateRequired } from '$lib/utils/validation';

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

	function handleFocus(): void {
		selectTask(null);
	}

	function handleKeydown(event: KeyboardEvent): void {
		if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
			event.preventDefault();
			const input = event.currentTarget as HTMLInputElement;
			const scope = input.closest('[data-keyboard-scope]');
			if (!scope) return;

			const allTasks = Array.from(
				scope.querySelectorAll<HTMLElement>('[data-task-id]')
			).filter((el) => !el.classList.contains('completed') && el.offsetParent !== null);

			const form = input.closest('.create-form')!;
			const formRect = form.getBoundingClientRect();

			if (event.key === 'ArrowUp') {
				const currentSectionId = (form as HTMLElement).dataset.sectionId;
				// Find the last visible task that appears before this form in the DOM
				for (let i = allTasks.length - 1; i >= 0; i--) {
					if (allTasks[i].getBoundingClientRect().top < formRect.top) {
						// If this task is in a different section (our section is empty),
						// go to that section's input instead
						if (allTasks[i].dataset.sectionId !== currentSectionId) {
							const allForms = Array.from(scope.querySelectorAll<HTMLElement>('.create-form'));
							const currentFormIndex = allForms.indexOf(form as HTMLElement);
							const prevForm = allForms[currentFormIndex - 1];
							if (prevForm) {
								const prevInput = prevForm.querySelector<HTMLInputElement>('.task-input');
								if (prevInput) {
									input.blur();
									prevInput.focus();
									prevInput.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
									return;
								}
							}
						}
						const taskId = Number(allTasks[i].dataset.taskId);
						if (!Number.isNaN(taskId)) {
							input.blur();
							allTasks[i].focus();
							selectTask(taskId);
							allTasks[i].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
						}
						return;
					}
				}
			} else {
				// Arrow Down: go to the next section's first task, or its input if empty
				const allForms = Array.from(scope.querySelectorAll<HTMLElement>('.create-form'));
				const currentFormIndex = allForms.indexOf(form as HTMLElement);
				const nextForm = allForms[currentFormIndex + 1];
				if (nextForm) {
					// Find the first visible task in the next section
					const nextSectionId = nextForm.dataset.sectionId;
					const nextTask = allTasks.find(
						(el) => el.dataset.sectionId === nextSectionId
					);
					if (nextTask) {
						const taskId = Number(nextTask.dataset.taskId);
						if (!Number.isNaN(taskId)) {
							input.blur();
							nextTask.focus();
							selectTask(taskId);
							nextTask.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
						}
					} else {
						// Next section has no tasks — focus its input
						const nextInput = nextForm.querySelector<HTMLInputElement>('.task-input');
						if (nextInput) {
							input.blur();
							nextInput.focus();
							nextInput.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
						}
					}
				}
			}
		} else if (event.key === 'Escape') {
			event.preventDefault();
			event.stopPropagation();
			title = '';
			dueDate = '';
			detecting = true;
			(event.currentTarget as HTMLInputElement).blur();
		}
	}

	async function submit(event: SubmitEvent): Promise<void> {
		event.preventDefault();
		if (!validateRequired({ 'Title': title })) return;
		const trimmed = title.trim();
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
		onkeydown={handleKeydown}
		onfocus={handleFocus}
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
