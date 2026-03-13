import { EditorView, keymap } from '@codemirror/view';
import { EditorState, type Extension } from '@codemirror/state';
import { markdown } from '@codemirror/lang-markdown';
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands';
import { autocompletion } from '@codemirror/autocomplete';
import { notebookTheme } from './theme';
import { livePreview } from './livePreview';
import { checkboxWidgets } from './checkboxWidgets';
import { createMentionWidgets } from './mentionWidgets';
import { createMentionCompletion, type MentionData } from './mentionCompletion';
import { listKeymap } from './listKeymap';

export interface EditorCallbacks {
	onChange: (content: string) => void;
	onBlur: () => void;
	onCheckboxNewline?: () => void;
	onNavigate?: (type: string, id: number, slug?: string) => void;
}

export interface NotebookEditor {
	view: EditorView;
	setContent: (text: string) => void;
	getContent: () => string;
	destroy: () => void;
}

export function createEditor(
	container: HTMLElement,
	initialContent: string,
	callbacks: EditorCallbacks,
	mentionData: MentionData
): NotebookEditor {
	const mentionCompletion = createMentionCompletion(mentionData);
	const mentionWidgets = createMentionWidgets(mentionData.pages);

	// Detect Enter on an unlinked checkbox line to trigger task generation
	const UNLINKED_CHECKBOX_RE = /^(\s*)(-|\*|\+)\s\[ \]\s(.+)$/;
	const checkboxNewlineKeymap: import('@codemirror/view').KeyBinding[] = callbacks.onCheckboxNewline
		? [
				{
					key: 'Enter',
					run(view) {
						const head = view.state.selection.main.head;
						const line = view.state.doc.lineAt(head);
						if (
							head === line.to &&
							UNLINKED_CHECKBOX_RE.test(line.text) &&
							!line.text.includes('[[task:')
						) {
							// Schedule callback after the document updates from the Enter keypress
							setTimeout(() => callbacks.onCheckboxNewline!(), 0);
						}
						return false; // Let listKeymap handle the actual Enter behavior
					}
				}
			]
		: [];

	const extensions: Extension[] = [
		history(),
		keymap.of([...checkboxNewlineKeymap, ...listKeymap, ...historyKeymap, ...defaultKeymap]),
		markdown(),
		notebookTheme,
		livePreview,
		checkboxWidgets,
		mentionWidgets,
		autocompletion({
			override: mentionCompletion,
			activateOnTyping: true,
			defaultKeymap: true
		}),
		EditorView.updateListener.of((update) => {
			if (update.docChanged) {
				callbacks.onChange(update.state.doc.toString());
			}
		}),
		EditorView.domEventHandlers({
			focusout: () => {
				callbacks.onBlur();
			},
			click: (event: MouseEvent, view: EditorView) => {
				if (!(event.ctrlKey || event.metaKey)) return false;
				const chip = (event.target as HTMLElement).closest?.('.cm-mention-chip') as HTMLElement | null;
				if (!chip?.dataset.entityType || !chip.dataset.entityId) return false;
				event.preventDefault();
				const type = chip.dataset.entityType;
				const id = Number(chip.dataset.entityId);
				const slug = chip.dataset.entitySlug;
				callbacks.onNavigate?.(type, id, slug);
				return true;
			},
			keydown: (event: KeyboardEvent, view: EditorView) => {
				if (event.key === 'Control' || event.key === 'Meta') {
					view.dom.closest('.cm-editor')?.classList.add('cm-ctrl-held');
				}
				return false;
			},
			keyup: (event: KeyboardEvent, view: EditorView) => {
				if (event.key === 'Control' || event.key === 'Meta') {
					view.dom.closest('.cm-editor')?.classList.remove('cm-ctrl-held');
				}
				return false;
			},
			blur: (_event: FocusEvent, view: EditorView) => {
				view.dom.closest('.cm-editor')?.classList.remove('cm-ctrl-held');
				return false;
			}
		}),
		EditorView.contentAttributes.of({ spellcheck: 'true' }),
		EditorView.lineWrapping
	];

	const state = EditorState.create({
		doc: initialContent,
		extensions
	});

	const view = new EditorView({ state, parent: container });

	function setContent(text: string) {
		const currentDoc = view.state.doc.toString();
		if (currentDoc === text) return;
		view.dispatch({
			changes: { from: 0, to: view.state.doc.length, insert: text }
		});
	}

	function getContent(): string {
		return view.state.doc.toString();
	}

	function destroy() {
		view.destroy();
	}

	return { view, setContent, getContent, destroy };
}
