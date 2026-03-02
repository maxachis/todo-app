import type { CompletionContext, CompletionResult, CompletionSource } from '@codemirror/autocomplete';

export interface MentionData {
	people: { id: number; first_name: string; last_name: string }[];
	pages: { id: number; title: string }[];
	tasks: { id: number; title: string }[];
	orgs: { id: number; name: string }[];
	projects: { id: number; name: string }[];
}

const TYPE_BADGES: Record<string, string> = {
	person: '\u{1F464}',
	page: '\u{1F4C4}',
	task: '\u2713',
	org: '\u{1F3E2}',
	project: '\u{1F4CB}'
};

function personCompletion(data: MentionData): CompletionSource {
	return (context: CompletionContext): CompletionResult | null => {
		const textBefore = context.state.doc.sliceString(0, context.pos);
		const match = textBefore.match(/(?:^|[\s(])@([a-zA-Z]*)$/);
		if (!match) return null;

		const query = match[1].toLowerCase();
		const atPos = context.pos - match[0].length + (match[0].startsWith('@') ? 0 : 1);

		const options = data.people
			.filter((p) => {
				const fullName = `${p.first_name} ${p.last_name}`.toLowerCase();
				return fullName.includes(query);
			})
			.slice(0, 8)
			.map((p) => {
				const label = `${p.first_name} ${p.last_name}`;
				return {
					label: `${TYPE_BADGES.person} ${label}`,
					displayLabel: `${TYPE_BADGES.person} ${label}`,
					detail: 'person',
					apply: `@[person:${p.id}|${label}]`
				};
			});

		if (options.length === 0) return null;

		return {
			from: atPos,
			options,
			filter: false
		};
	};
}

function entityCompletion(data: MentionData): CompletionSource {
	return (context: CompletionContext): CompletionResult | null => {
		const textBefore = context.state.doc.sliceString(0, context.pos);
		const match = textBefore.match(/\[\[([^\]]*)$/);
		if (!match) return null;

		const query = match[1].toLowerCase();
		const bracketPos = context.pos - match[0].length;

		interface EntityOption {
			type: string;
			id: number;
			label: string;
		}

		const results: EntityOption[] = [];

		for (const pg of data.pages) {
			if (pg.title.toLowerCase().includes(query)) {
				results.push({ type: 'page', id: pg.id, label: pg.title });
			}
		}
		for (const t of data.tasks) {
			if (t.title.toLowerCase().includes(query)) {
				results.push({ type: 'task', id: t.id, label: t.title });
			}
		}
		for (const o of data.orgs) {
			if (o.name.toLowerCase().includes(query)) {
				results.push({ type: 'org', id: o.id, label: o.name });
			}
		}
		for (const p of data.projects) {
			if (p.name.toLowerCase().includes(query)) {
				results.push({ type: 'project', id: p.id, label: p.name });
			}
		}

		const options = results.slice(0, 12).map((r) => ({
			label: `${TYPE_BADGES[r.type] || ''} ${r.label}`,
			displayLabel: `${TYPE_BADGES[r.type] || ''} ${r.label}`,
			detail: r.type,
			apply: `[[${r.type}:${r.id}|${r.label}]]`
		}));

		if (options.length === 0) return null;

		return {
			from: bracketPos,
			options,
			filter: false
		};
	};
}

export function createMentionCompletion(data: MentionData): CompletionSource[] {
	return [personCompletion(data), entityCompletion(data)];
}
