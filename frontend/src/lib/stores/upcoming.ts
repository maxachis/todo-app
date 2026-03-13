import { derived, writable } from 'svelte/store';

import { api, type UpcomingTask } from '$lib';

export const upcomingStore = writable<UpcomingTask[]>([]);

export const dueTaskCount = derived(upcomingStore, ($tasks) => {
	const today = new Date().toISOString().slice(0, 10);
	return $tasks.filter((t) => t.due_date !== null && t.due_date <= today).length;
});

export async function loadUpcoming(): Promise<void> {
	const tasks = await api.upcoming.get();
	upcomingStore.set(tasks);
}

export function removeUpcomingTask(taskId: number): void {
	upcomingStore.update((tasks) => tasks.filter((t) => t.id !== taskId));
}
