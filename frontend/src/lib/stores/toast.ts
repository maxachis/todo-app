import { writable } from 'svelte/store';

export interface Toast {
  id: string;
  message: string;
  type?: 'info' | 'success' | 'error';
  actionLabel?: string;
  onAction?: () => void;
}

export const toastStore = writable<Toast[]>([]);

const DEFAULT_TIMEOUT_MS = 5000;

export function addToast(toast: Omit<Toast, 'id'>, timeoutMs = DEFAULT_TIMEOUT_MS): string {
  const id = crypto.randomUUID();
  toastStore.update((toasts) => [...toasts, { id, ...toast }]);

  if (timeoutMs > 0) {
    setTimeout(() => {
      dismissToast(id);
    }, timeoutMs);
  }

  return id;
}

export function dismissToast(id: string): void {
  toastStore.update((toasts) => toasts.filter((toast) => toast.id !== id));
}
