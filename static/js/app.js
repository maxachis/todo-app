/* ============================================
   ToDo App — Main JavaScript
   Features: SortableJS, toasts, keyboard nav,
   emoji picker, markdown live-editor
   ============================================ */

// ─── Utilities ───────────────────────────────

function getCsrfToken() {
  var cookie = document.cookie.split(";").find(function(c) {
    return c.trim().startsWith("csrftoken=");
  });
  return cookie ? cookie.split("=")[1] : "";
}

/**
 * Persist a task move to the server without swapping DOM.
 * On success: no-op (DOM already reflects the change).
 * On failure: full GET refresh to restore correct state.
 */
function postMove(taskId, data) {
  fetch("/tasks/" + taskId + "/move/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCsrfToken(),
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams(data)
  }).then(function(resp) {
    if (!resp.ok) {
      htmx.ajax("GET", window.location.pathname, {
        target: "#center-panel",
        swap: "innerHTML"
      });
    }
  });
}

// ─── Toast ───────────────────────────────────

function dismissToast() {
  var toast = document.getElementById("undo-toast");
  if (toast) {
    toast.remove();
  }
}

function setupToastDismiss() {
  var toast = document.getElementById("undo-toast");
  if (toast) {
    var timeout = parseInt(toast.dataset.autoDismiss) || 5000;
    setTimeout(function() {
      if (toast && toast.parentNode) {
        toast.style.animation = "toastOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
        toast.addEventListener("animationend", function() {
          if (toast.parentNode) toast.remove();
        });
      }
    }, timeout);
  }
}

// ─── Auto-Focus after HTMX swap ─────────────

var lastFocusedInputSelector = null;

function trackFormFocus() {
  document.addEventListener("focusin", function(e) {
    var el = e.target;
    if (el.matches(".inline-form input[type='text'], .task-form input[type='text'], .section-form input[type='text'], .tag-form input[type='text']")) {
      var form = el.closest("form");
      if (form) {
        // Build a selector to re-find this input after swap
        if (form.classList.contains("task-form")) {
          var section = form.closest(".section");
          if (section) {
            lastFocusedInputSelector = '.section[data-section-id="' + section.dataset.sectionId + '"] .task-form input[name="title"]';
          }
        } else if (form.classList.contains("section-form")) {
          lastFocusedInputSelector = '.section-form input[name="name"]';
        } else if (form.classList.contains("tag-form")) {
          lastFocusedInputSelector = '.tag-form input[name="name"]';
        } else if (form.closest(".sidebar")) {
          lastFocusedInputSelector = '.sidebar .inline-form input[name="name"]';
        }
      }
    }
  });
}

function restoreFocus() {
  if (lastFocusedInputSelector) {
    var el = document.querySelector(lastFocusedInputSelector);
    if (el) {
      el.focus();
    }
    lastFocusedInputSelector = null;
  }
}

// ─── SortableJS Init ─────────────────────────

var sortableInstances = [];

function destroySortables() {
  sortableInstances.forEach(function(s) {
    try {
      if (s && s.destroy) s.destroy();
    } catch (ex) {
      // Element may have been removed by HTMX swap
    }
  });
  sortableInstances = [];
}

function initSortable() {
  destroySortables();

  document.querySelectorAll(".sortable-tasks").forEach(function(el) {
    var parentTaskId = el.dataset.parentTaskId || null;
    var sectionId = el.dataset.sectionId;

    var instance = new Sortable(el, {
      group: "tasks",
      animation: 150,
      ghostClass: "sortable-ghost",
      chosenClass: "sortable-chosen",
      handle: ".task-row",
      fallbackOnBody: true,
      swapThreshold: 0.65,
      onEnd: function(evt) {
        var taskId = evt.item.dataset.taskId;
        var dropZone = evt.to;
        var newSectionId = dropZone.dataset.sectionId;
        var newParentId = dropZone.dataset.parentTaskId || "null";
        var newIndex = evt.newIndex;

        // Update data attributes on the moved element
        evt.item.dataset.parentId = newParentId === "null" ? "" : newParentId;
        evt.item.dataset.sectionId = newSectionId;

        // SortableJS already moved the DOM element — just persist silently
        postMove(taskId, {
          section: newSectionId,
          position: newIndex * 10,
          parent: newParentId
        });
      }
    });
    sortableInstances.push(instance);
  });

  // Sidebar list drop targets for cross-list moves
  document.querySelectorAll(".list-nav-item").forEach(function(el) {
    var instance = new Sortable(el, {
      group: {
        name: "tasks",
        put: true,
        pull: false
      },
      onAdd: function(evt) {
        var taskId = evt.item.dataset.taskId;
        var listId = evt.to.dataset.listId;

        htmx.ajax("POST", "/tasks/" + taskId + "/move/", {
          values: {
            list: listId,
            csrfmiddlewaretoken: getCsrfToken()
          },
          target: "#center-panel",
          swap: "innerHTML"
        });
      }
    });
    sortableInstances.push(instance);
  });
}

// ─── Keyboard Navigation ─────────────────────

var focusedTaskId = null;

function getVisibleTasks() {
  return Array.from(
    document.querySelectorAll("#center-panel .task-item:not(.completed)")
  );
}

function setTaskFocus(taskEl, loadDetail) {
  // Remove old focus from task-rows
  document.querySelectorAll(".task-row.keyboard-focus").forEach(function(el) {
    el.classList.remove("keyboard-focus");
  });
  if (taskEl) {
    var row = taskEl.querySelector(":scope > .task-row");
    if (row) {
      row.classList.add("keyboard-focus");
    }
    focusedTaskId = taskEl.dataset.taskId;
    // Scroll into view if needed
    taskEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
    // Load task detail in right sidebar
    if (loadDetail) {
      htmx.ajax("GET", "/tasks/" + focusedTaskId + "/detail/", {
        target: "#detail-panel",
        swap: "innerHTML"
      });
    }
  } else {
    focusedTaskId = null;
  }
}

function restoreTaskFocus() {
  if (focusedTaskId) {
    var el = document.querySelector('.task-item[data-task-id="' + focusedTaskId + '"]');
    if (el) {
      setTaskFocus(el);
    } else {
      focusedTaskId = null;
    }
  }
}

function initKeyboardNav() {
  console.log("[keyboard-nav] initialized");

  // Click on a task row → highlight + load detail (skip checkbox clicks)
  document.addEventListener("click", function(e) {
    if (e.target.closest(".checkbox")) return;
    var row = e.target.closest(".task-row");
    if (!row) return;
    var taskItem = row.closest(".task-item");
    if (taskItem) {
      setTaskFocus(taskItem, true);
    }
  });

  document.addEventListener("keydown", function(e) {
    // Don't intercept when input/textarea/contenteditable is focused
    var tag = e.target.tagName.toLowerCase();
    if (tag === "input" || tag === "textarea" || e.target.isContentEditable) {
      return;
    }

    // Only handle navigation keys
    var navKeys = ["ArrowDown", "ArrowUp", "j", "k", "Tab", "x", "Escape"];
    if (navKeys.indexOf(e.key) === -1) return;

    var tasks = getVisibleTasks();
    if (tasks.length === 0) {
      console.log("[keyboard-nav] no visible tasks found");
      return;
    }

    var currentIndex = -1;
    if (focusedTaskId) {
      for (var i = 0; i < tasks.length; i++) {
        if (tasks[i].dataset.taskId === focusedTaskId) {
          currentIndex = i;
          break;
        }
      }
    }

    if (e.key === "ArrowDown" || e.key === "j") {
      e.preventDefault();
      var nextIndex = currentIndex + 1;
      if (nextIndex >= tasks.length) nextIndex = 0;
      setTaskFocus(tasks[nextIndex], true);
    } else if (e.key === "ArrowUp" || e.key === "k") {
      e.preventDefault();
      var prevIndex = currentIndex - 1;
      if (prevIndex < 0) prevIndex = tasks.length - 1;
      setTaskFocus(tasks[prevIndex], true);
    } else if (e.key === "Tab" && focusedTaskId) {
      e.preventDefault();
      var focused = document.querySelector('.task-item[data-task-id="' + focusedTaskId + '"]');
      if (!focused) return;

      if (e.shiftKey) {
        // Outdent: move task from parent's subtask zone to grandparent's container
        var currentParentId = focused.dataset.parentId;
        if (!currentParentId) return; // Already top-level, nothing to outdent

        var parentEl = document.querySelector('.task-item[data-task-id="' + currentParentId + '"]');
        if (!parentEl) return;

        var grandparentId = parentEl.dataset.parentId || "";
        // Target container: the .sortable-tasks that contains the parent element
        var targetContainer = parentEl.parentNode;

        // Move focused element after the parent in the target container
        if (parentEl.nextSibling) {
          targetContainer.insertBefore(focused, parentEl.nextSibling);
        } else {
          targetContainer.appendChild(focused);
        }

        // Update data attribute and visual depth
        focused.dataset.parentId = grandparentId;
        var parentDepth = parseInt(parentEl.style.paddingLeft) || 0;
        focused.style.paddingLeft = parentDepth + "em";

        // Persist silently
        postMove(focusedTaskId, {
          parent: grandparentId || "null"
        });
      } else {
        // Indent: move task into previous sibling's subtask drop zone
        if (currentIndex <= 0) return;

        // Find previous visible sibling (the task right above in the flat list)
        var prevTask = tasks[currentIndex - 1];
        var prevTaskId = prevTask.dataset.taskId;

        // Find the subtask drop zone inside the previous task
        var dropZone = prevTask.querySelector(":scope > .subtask-drop-zone");
        if (!dropZone) return;

        // Move focused element into the drop zone
        dropZone.appendChild(focused);

        // Update data attribute and visual depth
        focused.dataset.parentId = prevTaskId;
        var prevDepth = parseInt(prevTask.style.paddingLeft) || 0;
        focused.style.paddingLeft = (prevDepth + 1) + "em";

        // Persist silently
        postMove(focusedTaskId, {
          parent: prevTaskId
        });
      }
    } else if (e.key === "x" && focusedTaskId) {
      // Quick complete
      var focused = document.querySelector('.task-item[data-task-id="' + focusedTaskId + '"]');
      if (focused) {
        var checkbox = focused.querySelector(".checkbox");
        if (checkbox) checkbox.click();
      }
    } else if (e.key === "Escape") {
      setTaskFocus(null);
    }
  });
}

// ─── Emoji Picker ────────────────────────────

var emojiPickerEl = null;
var emojiPickerTarget = null;
var emojiPickerTrigger = null;

function createEmojiPicker() {
  if (emojiPickerEl) return emojiPickerEl;

  var picker = document.createElement("div");
  picker.className = "emoji-picker";
  picker.style.display = "none";

  // Search bar
  var searchDiv = document.createElement("div");
  searchDiv.className = "emoji-picker-search";
  var searchInput = document.createElement("input");
  searchInput.type = "text";
  searchInput.placeholder = "Search emoji...";
  searchDiv.appendChild(searchInput);
  picker.appendChild(searchDiv);

  // Grid container
  var gridContainer = document.createElement("div");
  gridContainer.className = "emoji-picker-grid";
  picker.appendChild(gridContainer);

  // Populate
  function renderEmojis(filter) {
    gridContainer.innerHTML = "";
    var lowerFilter = (filter || "").toLowerCase();

    if (typeof EMOJI_DATA === "undefined") return;

    EMOJI_DATA.forEach(function(cat) {
      var filtered = cat.emojis;
      if (lowerFilter) {
        filtered = cat.emojis.filter(function(em) {
          return em.n.indexOf(lowerFilter) !== -1;
        });
      }
      if (filtered.length === 0) return;

      var label = document.createElement("div");
      label.className = "emoji-category-label";
      label.textContent = cat.name;
      gridContainer.appendChild(label);

      var grid = document.createElement("div");
      grid.className = "emoji-grid";

      filtered.forEach(function(em) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "emoji-btn";
        btn.textContent = em.e;
        btn.title = em.n;
        btn.addEventListener("click", function() {
          selectEmoji(em.e);
        });
        grid.appendChild(btn);
      });

      gridContainer.appendChild(grid);
    });
  }

  // Debounced search
  var searchTimer = null;
  searchInput.addEventListener("input", function() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function() {
      renderEmojis(searchInput.value);
    }, 150);
  });

  renderEmojis("");
  document.body.appendChild(picker);
  emojiPickerEl = picker;
  return picker;
}

function selectEmoji(emoji) {
  if (emojiPickerTarget) {
    emojiPickerTarget.value = emoji;
  }
  var trigger = emojiPickerTrigger;
  if (trigger) {
    trigger.textContent = emoji;
  }
  closeEmojiPicker();

  // Auto-submit sidebar list edit form after emoji selection
  if (trigger) {
    var editForm = trigger.closest(".list-nav-edit-form");
    if (editForm) {
      htmx.trigger(editForm, "submit");
    }
  }
}

function openEmojiPicker(triggerBtn) {
  var picker = createEmojiPicker();
  var form = triggerBtn.closest("form");
  var targetName = triggerBtn.dataset.emojiTarget;
  emojiPickerTarget = form ? form.querySelector('input[name="' + targetName + '"]') : null;
  emojiPickerTrigger = triggerBtn;

  // Position near trigger
  var rect = triggerBtn.getBoundingClientRect();
  var pickerWidth = 320;
  var pickerHeight = 360;

  var left = rect.left;
  var top = rect.bottom + 4;

  // Keep on screen
  if (left + pickerWidth > window.innerWidth) {
    left = window.innerWidth - pickerWidth - 8;
  }
  if (top + pickerHeight > window.innerHeight) {
    top = rect.top - pickerHeight - 4;
  }

  picker.style.left = left + "px";
  picker.style.top = top + "px";
  picker.style.display = "flex";

  // Focus search
  var searchInput = picker.querySelector("input");
  if (searchInput) {
    searchInput.value = "";
    // Re-render with no filter
    var gridContainer = picker.querySelector(".emoji-picker-grid");
    if (gridContainer) {
      renderAllEmojis(gridContainer, "");
    }
    setTimeout(function() { searchInput.focus(); }, 50);
  }
}

function renderAllEmojis(gridContainer, filter) {
  gridContainer.innerHTML = "";
  var lowerFilter = (filter || "").toLowerCase();

  if (typeof EMOJI_DATA === "undefined") return;

  EMOJI_DATA.forEach(function(cat) {
    var filtered = cat.emojis;
    if (lowerFilter) {
      filtered = cat.emojis.filter(function(em) {
        return em.n.indexOf(lowerFilter) !== -1;
      });
    }
    if (filtered.length === 0) return;

    var label = document.createElement("div");
    label.className = "emoji-category-label";
    label.textContent = cat.name;
    gridContainer.appendChild(label);

    var grid = document.createElement("div");
    grid.className = "emoji-grid";

    filtered.forEach(function(em) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "emoji-btn";
      btn.textContent = em.e;
      btn.title = em.n;
      btn.addEventListener("click", function() {
        selectEmoji(em.e);
      });
      grid.appendChild(btn);
    });

    gridContainer.appendChild(grid);
  });
}

function closeEmojiPicker() {
  if (emojiPickerEl) {
    emojiPickerEl.style.display = "none";
  }
  emojiPickerTarget = null;
  emojiPickerTrigger = null;
}

function initEmojiPickers() {
  document.querySelectorAll(".emoji-trigger").forEach(function(btn) {
    // Avoid duplicate listeners by marking
    if (btn._emojiBound) return;
    btn._emojiBound = true;

    btn.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      if (emojiPickerEl && emojiPickerEl.style.display !== "none" && emojiPickerTrigger === btn) {
        closeEmojiPicker();
      } else {
        openEmojiPicker(btn);
      }
    });

    // If the hidden input already has a value, show it on the trigger
    var form = btn.closest("form");
    var targetName = btn.dataset.emojiTarget;
    if (form) {
      var hiddenInput = form.querySelector('input[name="' + targetName + '"]');
      if (hiddenInput && hiddenInput.value) {
        btn.textContent = hiddenInput.value;
      }
    }
  });
}

// Close picker on outside click or Escape
document.addEventListener("click", function(e) {
  if (emojiPickerEl && emojiPickerEl.style.display !== "none") {
    if (!emojiPickerEl.contains(e.target) && !e.target.classList.contains("emoji-trigger")) {
      closeEmojiPicker();
    }
  }
});
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape" && emojiPickerEl && emojiPickerEl.style.display !== "none") {
    closeEmojiPicker();
  }
});

// ─── Markdown Live Editor ────────────────────

function initMarkdownEditor() {
  var editor = document.getElementById("md-editor");
  var textarea = document.getElementById("notes");
  if (!editor || !textarea) return;

  var isRendering = false;
  var activeBlockIndex = -1;

  // Parse markdown text into blocks
  function parseBlocks(text) {
    if (!text) return [{ type: "p", raw: "" }];
    var lines = text.split("\n");
    var blocks = [];
    var i = 0;

    while (i < lines.length) {
      var line = lines[i];

      // Code fence
      if (line.match(/^```/)) {
        var lang = line.slice(3).trim();
        var codeLines = [];
        i++;
        while (i < lines.length && !lines[i].match(/^```/)) {
          codeLines.push(lines[i]);
          i++;
        }
        i++; // skip closing fence
        blocks.push({ type: "code", raw: "```" + lang + "\n" + codeLines.join("\n") + "\n```", content: codeLines.join("\n"), lang: lang });
        continue;
      }

      // Heading
      var headingMatch = line.match(/^(#{1,3})\s+(.*)/);
      if (headingMatch) {
        blocks.push({ type: "h" + headingMatch[1].length, raw: line, content: headingMatch[2] });
        i++;
        continue;
      }

      // HR
      if (line.match(/^(---|\*\*\*|___)\s*$/)) {
        blocks.push({ type: "hr", raw: line });
        i++;
        continue;
      }

      // Blockquote
      if (line.match(/^>\s?/)) {
        var quoteLines = [];
        while (i < lines.length && lines[i].match(/^>\s?/)) {
          quoteLines.push(lines[i].replace(/^>\s?/, ""));
          i++;
        }
        blocks.push({ type: "blockquote", raw: quoteLines.map(function(l) { return "> " + l; }).join("\n"), content: quoteLines.join("\n") });
        continue;
      }

      // Unordered list
      if (line.match(/^[\-\*]\s/)) {
        var listLines = [];
        while (i < lines.length && lines[i].match(/^[\-\*]\s/)) {
          listLines.push(lines[i].replace(/^[\-\*]\s/, ""));
          i++;
        }
        blocks.push({ type: "ul", raw: listLines.map(function(l) { return "- " + l; }).join("\n"), items: listLines });
        continue;
      }

      // Ordered list
      if (line.match(/^\d+\.\s/)) {
        var listLines = [];
        while (i < lines.length && lines[i].match(/^\d+\.\s/)) {
          listLines.push(lines[i].replace(/^\d+\.\s/, ""));
          i++;
        }
        blocks.push({ type: "ol", raw: listLines.map(function(l, idx) { return (idx + 1) + ". " + l; }).join("\n"), items: listLines });
        continue;
      }

      // Empty line
      if (line.trim() === "") {
        // Skip empty lines between blocks
        i++;
        continue;
      }

      // Paragraph: collect consecutive non-special lines
      var paraLines = [];
      while (i < lines.length && lines[i].trim() !== "" && !lines[i].match(/^(#{1,3}\s|```|---|\*\*\*|___|>\s?|[\-\*]\s|\d+\.\s)/)) {
        paraLines.push(lines[i]);
        i++;
      }
      blocks.push({ type: "p", raw: paraLines.join("\n"), content: paraLines.join("\n") });
    }

    if (blocks.length === 0) {
      blocks.push({ type: "p", raw: "", content: "" });
    }
    return blocks;
  }

  // Render inline markdown to HTML
  function renderInline(text) {
    if (!text) return "";
    var html = text;
    // Escape HTML
    html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/__(.+?)__/g, "<strong>$1</strong>");
    // Italic
    html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");
    html = html.replace(/_(.+?)_/g, "<em>$1</em>");
    // Strikethrough
    html = html.replace(/~~(.+?)~~/g, "<del>$1</del>");
    // Inline code
    html = html.replace(/`(.+?)`/g, "<code>$1</code>");
    // Links
    html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    return html;
  }

  // Render a block to HTML
  function renderBlock(block) {
    switch (block.type) {
      case "h1": return "<h1>" + renderInline(block.content) + "</h1>";
      case "h2": return "<h2>" + renderInline(block.content) + "</h2>";
      case "h3": return "<h3>" + renderInline(block.content) + "</h3>";
      case "hr": return "<hr>";
      case "code":
        var escaped = (block.content || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        return "<pre><code>" + escaped + "</code></pre>";
      case "blockquote":
        return "<blockquote>" + renderInline(block.content) + "</blockquote>";
      case "ul":
        return "<ul>" + block.items.map(function(item) { return "<li>" + renderInline(item) + "</li>"; }).join("") + "</ul>";
      case "ol":
        return "<ol>" + block.items.map(function(item) { return "<li>" + renderInline(item) + "</li>"; }).join("") + "</ol>";
      case "p":
      default:
        return "<p>" + renderInline(block.content || "") + "</p>";
    }
  }

  // Render all blocks into the editor
  function renderEditor(blocks, activeIdx) {
    isRendering = true;
    var html = "";
    blocks.forEach(function(block, idx) {
      if (idx === activeIdx) {
        // Show raw markdown for active block
        var rawEscaped = (block.raw || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        html += '<div class="md-block md-block-active" data-block-idx="' + idx + '">' + rawEscaped + '</div>';
      } else {
        html += '<div class="md-block" data-block-idx="' + idx + '">' + renderBlock(block) + '</div>';
      }
    });

    // Save cursor offset
    var sel = window.getSelection();
    var cursorOffset = 0;
    if (sel.rangeCount > 0 && editor.contains(sel.anchorNode)) {
      cursorOffset = sel.anchorOffset;
    }

    editor.innerHTML = html;

    // Restore cursor into active block
    if (activeIdx >= 0) {
      var activeEl = editor.querySelector('.md-block-active');
      if (activeEl && activeEl.firstChild) {
        try {
          var range = document.createRange();
          var textNode = activeEl.firstChild;
          var offset = Math.min(cursorOffset, textNode.length || 0);
          range.setStart(textNode, offset);
          range.collapse(true);
          sel.removeAllRanges();
          sel.addRange(range);
        } catch (ex) {
          // Fallback: just place cursor at end
        }
      }
    }

    isRendering = false;
  }

  // Get current blocks from editor text
  function getEditorText() {
    var blocks = editor.querySelectorAll(".md-block");
    var parts = [];
    blocks.forEach(function(blockEl) {
      var idx = parseInt(blockEl.dataset.blockIdx);
      if (blockEl.classList.contains("md-block-active")) {
        parts.push(blockEl.textContent);
      } else {
        // Use stored raw from data
        parts.push(currentBlocks[idx] ? currentBlocks[idx].raw : blockEl.textContent);
      }
    });
    return parts.join("\n\n");
  }

  var currentBlocks = parseBlocks(textarea.value);

  // Initial render — no active block
  renderEditor(currentBlocks, -1);

  // Track which block the cursor is in
  document.addEventListener("selectionchange", function() {
    if (isRendering) return;
    if (!editor.contains(document.activeElement) && document.activeElement !== editor) return;

    var sel = window.getSelection();
    if (!sel.rangeCount) return;

    var node = sel.anchorNode;
    var blockEl = null;

    // Walk up to find .md-block
    while (node && node !== editor) {
      if (node.nodeType === 1 && node.classList && node.classList.contains("md-block")) {
        blockEl = node;
        break;
      }
      node = node.parentNode;
    }

    if (blockEl) {
      var newIdx = parseInt(blockEl.dataset.blockIdx);
      if (newIdx !== activeBlockIndex) {
        // Save current active block's text before switching
        if (activeBlockIndex >= 0) {
          var oldActive = editor.querySelector('.md-block-active');
          if (oldActive && currentBlocks[activeBlockIndex]) {
            currentBlocks[activeBlockIndex].raw = oldActive.textContent;
            // Re-parse this single block
            var reparsed = parseBlocks(oldActive.textContent);
            if (reparsed.length > 0) {
              currentBlocks[activeBlockIndex] = reparsed[0];
            }
          }
        }
        activeBlockIndex = newIdx;
        renderEditor(currentBlocks, activeBlockIndex);
      }
    }
  });

  // Handle input in active block
  editor.addEventListener("input", function() {
    if (isRendering) return;
    // Update textarea with current content
    textarea.value = getEditorText();
  });

  // Paste as plain text
  editor.addEventListener("paste", function(e) {
    e.preventDefault();
    var text = e.clipboardData.getData("text/plain");
    document.execCommand("insertText", false, text);
  });

  // Handle Enter to create new block
  editor.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();

      // Save current active block
      if (activeBlockIndex >= 0) {
        var activeEl = editor.querySelector('.md-block-active');
        if (activeEl && currentBlocks[activeBlockIndex]) {
          currentBlocks[activeBlockIndex].raw = activeEl.textContent;
          var reparsed = parseBlocks(activeEl.textContent);
          if (reparsed.length > 0) {
            currentBlocks[activeBlockIndex] = reparsed[0];
          }
        }
      }

      // Insert new empty block after current
      var newBlock = { type: "p", raw: "", content: "" };
      var insertIdx = activeBlockIndex >= 0 ? activeBlockIndex + 1 : currentBlocks.length;
      currentBlocks.splice(insertIdx, 0, newBlock);
      activeBlockIndex = insertIdx;

      renderEditor(currentBlocks, activeBlockIndex);
      textarea.value = getEditorText();

      // Focus the new block
      var newBlockEl = editor.querySelector('.md-block-active');
      if (newBlockEl) {
        var range = document.createRange();
        range.setStart(newBlockEl, 0);
        range.collapse(true);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
      }
    }
  });

  // Sync to textarea before form submit
  document.addEventListener("htmx:configRequest", function(e) {
    if (e.detail.elt.closest && e.detail.elt.closest("form") === editor.closest("form")) {
      // Save active block
      if (activeBlockIndex >= 0) {
        var activeEl = editor.querySelector('.md-block-active');
        if (activeEl && currentBlocks[activeBlockIndex]) {
          currentBlocks[activeBlockIndex].raw = activeEl.textContent;
        }
      }
      textarea.value = getEditorText();
    }
  });

  // On blur, deactivate all blocks
  editor.addEventListener("blur", function() {
    if (isRendering) return;
    // Save active block
    if (activeBlockIndex >= 0) {
      var activeEl = editor.querySelector('.md-block-active');
      if (activeEl && currentBlocks[activeBlockIndex]) {
        currentBlocks[activeBlockIndex].raw = activeEl.textContent;
        var reparsed = parseBlocks(activeEl.textContent);
        if (reparsed.length > 0) {
          currentBlocks[activeBlockIndex] = reparsed[0];
        }
      }
    }
    activeBlockIndex = -1;
    // Small delay to avoid conflicts with selectionchange
    setTimeout(function() {
      if (document.activeElement !== editor && !editor.contains(document.activeElement)) {
        renderEditor(currentBlocks, -1);
        textarea.value = getEditorText();
      }
    }, 100);
  });
}

// ─── Sidebar List Name Edit ──────────────────

function initListNameEdit() {
  document.querySelectorAll(".list-nav-item").forEach(function(li) {
    if (li._editBound) return;
    li._editBound = true;

    var display = li.querySelector(".list-nav-display");
    var form = li.querySelector(".list-nav-edit-form");
    if (!display || !form) return;

    var nameInput = form.querySelector('input[name="name"]');

    // Double-click on display text enters edit mode
    display.addEventListener("dblclick", function(e) {
      e.preventDefault();
      e.stopPropagation();
      li.classList.add("editing");
      if (nameInput) {
        nameInput.focus();
        nameInput.select();
      }
    });

    // Prevent single-click navigation while editing, but allow form interactions
    li.addEventListener("click", function(e) {
      if (li.classList.contains("editing") && !form.contains(e.target)) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);

    li.addEventListener("htmx:confirm", function(e) {
      if (li.classList.contains("editing") && e.detail.elt === li) {
        e.preventDefault();
      }
    });

    if (nameInput) {
      // Enter submits the form
      nameInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
          e.preventDefault();
          htmx.trigger(form, "submit");
        } else if (e.key === "Escape") {
          e.preventDefault();
          cancelEdit(li);
        }
      });

      // Blur cancels edit (unless emoji picker is open or focus is in form)
      nameInput.addEventListener("blur", function(e) {
        setTimeout(function() {
          var pickerOpen = emojiPickerEl && emojiPickerEl.style.display !== "none";
          if (!form.contains(document.activeElement) && !pickerOpen) {
            cancelEdit(li);
          }
        }, 150);
      });
    }
  });
}

function cancelEdit(li) {
  li.classList.remove("editing");
  // Reset input values to original
  var nameInput = li.querySelector('.list-nav-edit-form input[name="name"]');
  var nameSpan = li.querySelector(".list-name");
  if (nameInput && nameSpan) {
    nameInput.value = nameSpan.textContent;
  }
  var emojiInput = li.querySelector('.list-nav-edit-form input[name="emoji"]');
  var emojiSpan = li.querySelector(".list-emoji");
  var emojiBtn = li.querySelector(".list-nav-edit-form .emoji-trigger");
  if (emojiInput && emojiSpan) {
    emojiInput.value = emojiSpan.textContent;
    if (emojiBtn) emojiBtn.textContent = emojiSpan.textContent || "+";
  }
}

// ─── Init & HTMX Hooks ──────────────────────

function initAll() {
  try { initSortable(); } catch (ex) { console.error("initSortable error:", ex); }
  setupToastDismiss();
  try { initEmojiPickers(); } catch (ex) { console.error("initEmojiPickers error:", ex); }
  try { initMarkdownEditor(); } catch (ex) { console.error("initMarkdownEditor error:", ex); }
  try { initListNameEdit(); } catch (ex) { console.error("initListNameEdit error:", ex); }
  restoreTaskFocus();
  restoreFocus();
}

// Re-init after HTMX swaps
document.addEventListener("htmx:afterSwap", function() {
  initAll();
});

// Init on page load
document.addEventListener("DOMContentLoaded", function() {
  trackFormFocus();
  initKeyboardNav();
  initAll();
});
