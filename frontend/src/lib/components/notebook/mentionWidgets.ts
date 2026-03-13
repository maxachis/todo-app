import {
	Decoration,
	type DecorationSet,
	EditorView,
	ViewPlugin,
	type ViewUpdate,
	WidgetType
} from '@codemirror/view';
import { RangeSetBuilder } from '@codemirror/state';

const PERSON_RE = /@\[person:(\d+)\|([^\]]+)\]/g;
const ENTITY_RE = /\[\[(page|task|org|project):(\d+)\|([^\]]+)\]\]/g;
const NEW_CONTACT_RE = /@new\[([^\]]+)\](?:\(([^)]*)\))?/g;

const TYPE_BADGES: Record<string, string> = {
	person: '\u{1F464}',
	task: '\u2713',
	page: '\u{1F4C4}',
	org: '\u{1F3E2}',
	project: '\u{1F4CB}'
};

class NewContactWidget extends WidgetType {
	readonly name: string;
	readonly notes: string;

	constructor(name: string, notes: string) {
		super();
		this.name = name;
		this.notes = notes;
	}

	eq(other: NewContactWidget): boolean {
		return this.name === other.name && this.notes === other.notes;
	}

	toDOM(): HTMLElement {
		const span = document.createElement('span');
		span.className = 'cm-mention-chip cm-mention-new';

		const badge = document.createElement('span');
		badge.className = 'cm-mention-badge';
		badge.textContent = '\u2795'; // ➕

		const label = document.createElement('span');
		label.className = 'cm-mention-label';
		label.textContent = this.name;

		span.appendChild(badge);
		span.appendChild(label);

		if (this.notes) {
			const notesEl = document.createElement('span');
			notesEl.className = 'cm-mention-notes';
			notesEl.textContent = ` (${this.notes})`;
			span.appendChild(notesEl);
		}

		return span;
	}

	ignoreEvent(): boolean {
		return false;
	}
}

class MentionWidget extends WidgetType {
	readonly type: string;
	readonly id: string;
	readonly label: string;
	readonly slug: string | undefined;

	constructor(type: string, id: string, label: string, slug?: string) {
		super();
		this.type = type;
		this.id = id;
		this.label = label;
		this.slug = slug;
	}

	eq(other: MentionWidget): boolean {
		return this.type === other.type && this.id === other.id && this.label === other.label;
	}

	toDOM(): HTMLElement {
		const span = document.createElement('span');
		span.className = 'cm-mention-chip';
		span.dataset.entityType = this.type;
		span.dataset.entityId = this.id;
		if (this.slug) {
			span.dataset.entitySlug = this.slug;
		}

		const badge = document.createElement('span');
		badge.className = 'cm-mention-badge';
		badge.textContent = TYPE_BADGES[this.type] || '';

		const label = document.createElement('span');
		label.className = 'cm-mention-label';
		label.textContent = this.label;

		span.appendChild(badge);
		span.appendChild(label);
		return span;
	}

	ignoreEvent(): boolean {
		return false;
	}
}

function buildDecorations(view: EditorView, pagesById: Map<number, string>): DecorationSet {
	const builder = new RangeSetBuilder<Decoration>();
	const doc = view.state.doc;
	const text = doc.toString();

	const decos: { from: number; to: number; deco: Decoration }[] = [];

	// Person mentions: @[person:ID|Label]
	let match: RegExpExecArray | null;
	PERSON_RE.lastIndex = 0;
	while ((match = PERSON_RE.exec(text)) !== null) {
		const from = match.index;
		const to = from + match[0].length;
		decos.push({
			from,
			to,
			deco: Decoration.replace({
				widget: new MentionWidget('person', match[1], match[2])
			})
		});
	}

	// Entity mentions: [[type:ID|Label]]
	ENTITY_RE.lastIndex = 0;
	while ((match = ENTITY_RE.exec(text)) !== null) {
		const from = match.index;
		const to = from + match[0].length;
		const entityType = match[1];
		const entityId = match[2];
		const slug = entityType === 'page' ? pagesById.get(Number(entityId)) : undefined;
		decos.push({
			from,
			to,
			deco: Decoration.replace({
				widget: new MentionWidget(entityType, entityId, match[3], slug)
			})
		});
	}

	// New contact drafts: @new[Name](notes)
	NEW_CONTACT_RE.lastIndex = 0;
	while ((match = NEW_CONTACT_RE.exec(text)) !== null) {
		const from = match.index;
		const to = from + match[0].length;
		decos.push({
			from,
			to,
			deco: Decoration.replace({
				widget: new NewContactWidget(match[1], match[2] || '')
			})
		});
	}

	// Sort by position
	decos.sort((a, b) => a.from - b.from);
	for (const { from, to, deco } of decos) {
		if (from < to) {
			builder.add(from, to, deco);
		}
	}

	return builder.finish();
}

export function createMentionWidgets(pages: { id: number; slug: string }[]) {
	const pagesById = new Map(pages.map((p) => [p.id, p.slug]));
	return ViewPlugin.fromClass(
		class {
			decorations: DecorationSet;
			constructor(view: EditorView) {
				this.decorations = buildDecorations(view, pagesById);
			}
			update(update: ViewUpdate) {
				if (update.docChanged || update.viewportChanged) {
					this.decorations = buildDecorations(update.view, pagesById);
				}
			}
		},
		{
			decorations: (v) => v.decorations
		}
	);
}
