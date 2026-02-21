import { writable } from 'svelte/store';

import { api, type UpcomingTask } from '$lib';

export const upcomingStore = writable<UpcomingTask[]>([]);

export async function loadUpcoming(): Promise<void> {
	const tasks = await api.upcoming.get();
	upcomingStore.set(tasks);
}
