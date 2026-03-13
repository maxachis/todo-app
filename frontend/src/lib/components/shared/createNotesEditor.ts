import { EditorView, keymap } from '@codemirror/view';
import { EditorState } from '@codemirror/state';
import { markdown } from '@codemirror/lang-markdown';
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands';
import { notebookTheme } from '../notebook/theme';
import { livePreview } from '../notebook/livePreview';
import { checkboxWidgets } from '../notebook/checkboxWidgets';
import { listKeymap } from '../notebook/listKeymap';

export interface NotesEditorInstance {
	view: EditorView;
	setContent: (text: string) => void;
	getContent: () => string;
	destroy: () => void;
}

export function createNotesEditor(
	container: HTMLElement,
	initialContent: string,
	callbacks: { onChange: (content: string) => void; onBlur: () => void }
): NotesEditorInstance {
	const state = EditorState.create({
		doc: initialContent,
		extensions: [
			history(),
			keymap.of([...listKeymap, ...historyKeymap, ...defaultKeymap]),
			markdown(),
			notebookTheme,
			EditorView.theme({
				'&': { height: 'auto', minHeight: '80px' },
				'.cm-scroller': { overflow: 'visible' }
			}),
			livePreview,
			checkboxWidgets,
			EditorView.updateListener.of((update) => {
				if (update.docChanged) {
					callbacks.onChange(update.state.doc.toString());
				}
			}),
			EditorView.domEventHandlers({
				focusout: () => {
					callbacks.onBlur();
				}
			}),
			EditorView.contentAttributes.of({ spellcheck: 'true' }),
			EditorView.lineWrapping
		]
	});

	const view = new EditorView({ state, parent: container });

	function setContent(text: string) {
		if (view.state.doc.toString() === text) return;
		view.dispatch({
			changes: { from: 0, to: view.state.doc.length, insert: text }
		});
	}

	return {
		view,
		setContent,
		getContent: () => view.state.doc.toString(),
		destroy: () => view.destroy()
	};
}
