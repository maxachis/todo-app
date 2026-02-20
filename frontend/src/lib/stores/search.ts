import { writable } from 'svelte/store';

import { api, type SearchResponse } from '$lib';

export const searchStore = writable<SearchResponse>({
  query: '',
  total_count: 0,
  results: []
});

let timer: ReturnType<typeof setTimeout> | null = null;

export function searchDebounced(query: string, delayMs = 300): Promise<SearchResponse> {
  if (timer) {
    clearTimeout(timer);
  }

  return new Promise((resolve, reject) => {
    timer = setTimeout(async () => {
      try {
        const result = await api.search.run(query);
        searchStore.set(result);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    }, delayMs);
  });
}

export async function performSearch(query: string): Promise<void> {
  const result = await api.search.run(query);
  searchStore.set(result);
}

export function clearSearch(): void {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
  searchStore.set({ query: '', total_count: 0, results: [] });
}
