type Direction = 'prev' | 'next';

export interface KeyboardOptions {
	getCurrentTaskId: () => number | null;
	onSelectTask: (taskId: number | null) => void | Promise<void>;
	onCompleteTask: (taskId: number) => void | Promise<void>;
	onDeleteTask: (taskId: number) => void | Promise<void>;
	onIndentTask: (taskId: number, parentId: number, sectionId: number) => void | Promise<void>;
	onOutdentTask: (taskId: number, sectionId: number) => void | Promise<void>;
	onCycleList: (direction: Direction) => void | Promise<void>;
}

function getVisibleTaskElements(node: HTMLElement): HTMLElement[] {
	return Array.from(node.querySelectorAll<HTMLElement>('[data-task-id]')).filter(
		(el) =>
			!el.classList.contains('completed') &&
			el.offsetParent !== null
	);
}

function toId(value: string | null): number | null {
	if (!value) return null;
	const id = Number(value);
	return Number.isNaN(id) ? null : id;
}

function scrollIntoView(el: HTMLElement): void {
	el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

function isTextEntryTarget(target: EventTarget | null): boolean {
	const el = target as HTMLElement | null;
	if (!el) return false;
	return !!el.closest('input, textarea, select, [contenteditable="true"]');
}

export function keyboard(node: HTMLElement, options: KeyboardOptions) {
	const handleKeydown = async (event: KeyboardEvent) => {
		const elements = getVisibleTaskElements(node);
		const ids = elements
			.map((el) => toId(el.dataset.taskId ?? null))
			.filter((id): id is number => id !== null);

		const currentId = options.getCurrentTaskId();
		const currentIndex = currentId === null ? -1 : ids.indexOf(currentId);
		const eventElement = (event.target as HTMLElement | null)?.closest<HTMLElement>('[data-task-id]');
		const eventElementId = toId(eventElement?.dataset.taskId ?? null);
		const resolvedCurrentId = currentIndex >= 0 ? currentId : eventElementId;
		const resolvedCurrentIndex =
			currentIndex >= 0
				? currentIndex
				: eventElementId === null
					? -1
					: ids.indexOf(eventElementId);
		const currentElement =
			resolvedCurrentIndex >= 0
				? elements[resolvedCurrentIndex]
				: eventElement ?? (resolvedCurrentId === null ? null : node.querySelector<HTMLElement>(`[data-task-id="${resolvedCurrentId}"]`));

		const selectByIndex = async (index: number): Promise<void> => {
			const target = elements[index];
			if (!target) return;
			const targetId = toId(target.dataset.taskId ?? null);
			if (targetId === null) return;
			await options.onSelectTask(targetId);
			scrollIntoView(target);
		};

		if ((event.key === 'ArrowDown' || event.key === 'j') && !event.ctrlKey) {
			event.preventDefault();
			const nextIndex = Math.min(elements.length - 1, currentIndex + 1);
			await selectByIndex(nextIndex < 0 ? 0 : nextIndex);
			return;
		}

		if ((event.key === 'ArrowUp' || event.key === 'k') && !event.ctrlKey) {
			event.preventDefault();
			const prevIndex = Math.max(0, currentIndex - 1);
			await selectByIndex(prevIndex);
			return;
		}

		if (event.key === 'Tab' && resolvedCurrentId !== null) {
			event.preventDefault();
			const currentSectionId = toId(currentElement?.dataset.sectionId ?? null);
			if (currentSectionId === null) return;
			const currentParentId = toId(currentElement?.dataset.parentId ?? null);
			if (event.shiftKey) {
				await options.onOutdentTask(resolvedCurrentId, currentSectionId);
				return;
			}
			let prevSameLevelId: number | null = null;
			let idx = resolvedCurrentIndex - 1;
			while (idx >= 0) {
				const sectionId = toId(elements[idx].dataset.sectionId ?? null);
				const parentId = toId(elements[idx].dataset.parentId ?? null);
				if (sectionId === currentSectionId && parentId === currentParentId) {
					prevSameLevelId = ids[idx];
					break;
				}
				idx -= 1;
			}
			if (prevSameLevelId !== null) {
				await options.onIndentTask(resolvedCurrentId, prevSameLevelId, currentSectionId);
			}
			return;
		}

		if (event.key === 'x' && currentId !== null) {
			event.preventDefault();
			await options.onCompleteTask(currentId);
			return;
		}

		if (event.key === 'Delete' && currentId !== null) {
			event.preventDefault();
			if (confirm('Delete this task?')) {
				await options.onDeleteTask(currentId);
			}
			return;
		}

		if (event.key === 'Escape') {
			event.preventDefault();
			await options.onSelectTask(null);
			return;
		}

		if (event.ctrlKey && (event.key === 'ArrowDown' || event.key === 'ArrowUp') && currentElement) {
			event.preventDefault();
			const direction = event.key === 'ArrowDown' ? 1 : -1;
			const currentSection = toId(currentElement.dataset.sectionId ?? null);
			if (currentSection === null) return;

			let idx = currentIndex + direction;
			while (idx >= 0 && idx < elements.length) {
				const candidate = elements[idx];
				const sectionId = toId(candidate.dataset.sectionId ?? null);
				if (sectionId !== null && sectionId !== currentSection) {
					await selectByIndex(idx);
					return;
				}
				idx += direction;
			}
			return;
		}

		if (event.ctrlKey && event.key === 'ArrowLeft') {
			event.preventDefault();
			await options.onCycleList('prev');
			return;
		}

		if (event.ctrlKey && event.key === 'ArrowRight') {
			event.preventDefault();
			await options.onCycleList('next');
		}
	};

	const handleWindowKeydownCapture = async (event: KeyboardEvent) => {
		if (event.key !== 'Tab') return;
		if (options.getCurrentTaskId() === null) return;
		if (isTextEntryTarget(event.target)) return;

		await handleKeydown(event);
		if (event.defaultPrevented) {
			event.stopPropagation();
		}
	};

	node.addEventListener('keydown', handleKeydown);
	window.addEventListener('keydown', handleWindowKeydownCapture, true);

	return {
		destroy() {
			node.removeEventListener('keydown', handleKeydown);
			window.removeEventListener('keydown', handleWindowKeydownCapture, true);
		}
	};
}
