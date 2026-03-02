import { EditorView, keymap } from '@codemirror/view';
import { EditorState, type Extension } from '@codemirror/state';
import { markdown } from '@codemirror/lang-markdown';
import { defaultKeymap, history, historyKeymap } from '@codemirror/commands';
import { autocompletion } from '@codemirror/autocomplete';
import { notebookTheme } from './theme';
import { livePreview } from './livePreview';
import { checkboxWidgets } from './checkboxWidgets';
import { mentionWidgets } from './mentionWidgets';
import { createMentionCompletion, type MentionData } from './mentionCompletion';
import { listKeymap } from './listKeymap';

export interface EditorCallbacks {
	onChange: (content: string) => void;
	onBlur: () => void;
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

	const extensions: Extension[] = [
		history(),
		keymap.of([...listKeymap, ...historyKeymap, ...defaultKeymap]),
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
