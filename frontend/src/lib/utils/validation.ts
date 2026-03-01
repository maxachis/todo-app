import { addToast } from '$lib/stores/toast';

type FieldValue = string | number | null | undefined | unknown[];

export function validateRequired(fields: Record<string, FieldValue>): boolean {
	const missing = Object.entries(fields)
		.filter(([, v]) => {
			if (v == null) return true;
			if (typeof v === 'string') return v.trim() === '';
			if (Array.isArray(v)) return v.length === 0;
			return false;
		})
		.map(([label]) => label);

	if (missing.length > 0) {
		addToast({
			message: `Required: ${missing.join(', ')}`,
			type: 'error'
		});
		return false;
	}
	return true;
}
