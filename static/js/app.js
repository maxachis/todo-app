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
 * Returns a promise that resolves when the server responds.
 */
function postMove(taskId, data) {
  return fetch("/tasks/" + taskId + "/move/", {
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

/**
 * Persist a section reorder to the server without swapping DOM.
 * On success: no-op (DOM already reflects the change).
 * On failure: full GET refresh to restore correct state.
 */
function postSectionMove(sectionId, data) {
  return fetch("/sections/" + sectionId + "/move/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCsrfToken(),
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams(data)
  }).then(function(resp) {
    if (!resp.ok) {
      console.error("[section-move] server returned " + resp.status);
      htmx.ajax("GET", window.location.pathname, {
        target: "#center-panel",
        swap: "innerHTML"
      });
    }
  }).catch(function(err) {
    console.error("[section-move] fetch failed:", err);
    htmx.ajax("GET", window.location.pathname, {
      target: "#center-panel",
      swap: "innerHTML"
    });
  });
}

/**
 * Persist a list reorder to the server without swapping DOM.
 * On success: no-op (DOM already reflects the change).
 * On failure: full GET refresh of the sidebar to restore correct state.
 */
function postListMove(listId, data) {
  return fetch("/lists/" + listId + "/move/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCsrfToken(),
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams(data)
  }).then(function(resp) {
    if (!resp.ok) {
      console.error("[list-move] server returned " + resp.status);
      htmx.ajax("GET", window.location.pathname, {
        target: "#center-panel",
        swap: "innerHTML"
      });
    }
  }).catch(function(err) {
    console.error("[list-move] fetch failed:", err);
    htmx.ajax("GET", window.location.pathname, {
      target: "#center-panel",
      swap: "innerHTML"
    });
  });
}

/**
 * Update subtask count labels on all parent tasks that have a
 * .subtask-collapse-toggle. Re-counts active and completed
 * subtask items in the DOM and refreshes the label text to show
 * both total and completed counts (e.g. "3 subtasks (1 done)").
 */
function updateSubtaskCounts() {
  document.querySelectorAll(".subtask-collapsible").forEach(function(details) {
    var toggle = details.querySelector(":scope > .subtask-collapse-toggle");
    if (!toggle) return;
    var countSpan = toggle.querySelector(".subtask-collapse-count");
    if (!countSpan) return;

    var dropZone = details.querySelector(":scope > .subtask-collapsible-content > .subtask-drop-zone");
    if (!dropZone) return;

    // Count direct children that are .task-item and not .completed
    var activeCount = dropZone.querySelectorAll(":scope > .task-item:not(.completed)").length;
    // Count completed subtasks
    var completedCount = 0;
    var completedGroup = details.querySelector(":scope > .subtask-collapsible-content > .subtask-completed-group");
    if (completedGroup) {
      completedCount = completedGroup.querySelectorAll(".subtask-completed-items > .task-item.completed").length;
    }

    var total = activeCount + completedCount;
    var label = total + " subtask" + (total !== 1 ? "s" : "");
    if (completedCount > 0) {
      label += " (" + completedCount + " done)";
    }
    countSpan.textContent = label;
  });
}

// ─── Toast ───────────────────────────────────

function dismissToast() {
  var toast = document.getElementById("undo-toast");
  if (toast) {
    toast.style.animation = "toastOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
    toast.addEventListener("animationend", function() {
      if (toast.parentNode) toast.remove();
    });
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
      delay: 150,
      delayOnTouchOnly: true,
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

  // Sidebar list drop targets for cross-list moves.
  // Use a non-existent handle so these child Sortable instances never
  // initiate drags (they only receive task drops via group.put).  This
  // prevents them from intercepting mousedown events that should reach
  // the parent #list-nav Sortable for list reordering.
  document.querySelectorAll(".list-nav-item").forEach(function(el) {
    var instance = new Sortable(el, {
      group: {
        name: "tasks",
        put: true,
        pull: false
      },
      sort: false,
      handle: ".task-drop-handle-none",
      filter: ".list-drag-handle",
      preventOnFilter: false,
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

  // Section reordering within a list.
  // The draggable element is a <details> whose <summary> is the
  // drag handle.  On mouseup the browser fires a "click" on the
  // <summary> which toggles the <details> open/close state.
  // We suppress that toggle during the drag to prevent a visual
  // snap-back or collapsed section after reordering.
  document.querySelectorAll(".sortable-sections").forEach(function(el) {
    var sectionDragClickBlocker = null;

    var instance = new Sortable(el, {
      animation: 150,
      ghostClass: "sortable-ghost",
      chosenClass: "sortable-chosen",
      handle: ".section-header",
      draggable: ".section",
      onStart: function(evt) {
        // Block the <summary> click that would toggle <details>
        sectionDragClickBlocker = function(e) { e.preventDefault(); };
        evt.item.addEventListener("click", sectionDragClickBlocker, true);
      },
      onEnd: function(evt) {
        // Remove the click blocker after a short delay so the
        // browser's pending click event is consumed first.
        var item = evt.item;
        setTimeout(function() {
          if (sectionDragClickBlocker) {
            item.removeEventListener("click", sectionDragClickBlocker, true);
            sectionDragClickBlocker = null;
          }
        }, 50);

        var sectionEl = evt.item;
        var sectionId = sectionEl.dataset.sectionId;
        // Prefer newDraggableIndex (counts only draggable children)
        // over newIndex (counts all element children) for accuracy
        var newIndex = typeof evt.newDraggableIndex === "number"
          ? evt.newDraggableIndex : evt.newIndex;

        postSectionMove(sectionId, {
          position: newIndex * 10
        });
      }
    });
    sortableInstances.push(instance);
  });

  // List reordering in the sidebar
  var listNav = document.getElementById("list-nav");
  if (listNav) {
    var instance = new Sortable(listNav, {
      animation: 150,
      ghostClass: "sortable-ghost",
      chosenClass: "sortable-chosen",
      handle: ".list-drag-handle",
      draggable: ".list-nav-item",
      onEnd: function(evt) {
        var listItem = evt.item;
        var listId = listItem.dataset.listId;
        // Prefer newDraggableIndex (counts only draggable children)
        var newIndex = typeof evt.newDraggableIndex === "number"
          ? evt.newDraggableIndex : evt.newIndex;

        postListMove(listId, {
          position: newIndex * 10
        });
      }
    });
    sortableInstances.push(instance);
  }
}

// ─── Keyboard Navigation ─────────────────────

var focusedTaskId = null;

function getVisibleTasks() {
  return Array.from(
    document.querySelectorAll("#center-panel .task-item:not(.completed)")
  ).filter(function(el) {
    // Exclude tasks inside collapsed <details> elements
    var node = el.parentElement;
    while (node && node.id !== "center-panel") {
      if (node.tagName === "DETAILS" && !node.open) {
        return false;
      }
      node = node.parentElement;
    }
    return true;
  });
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
      }).then(function() {
        openDetailPanel();
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
  // Click outside any task row → clear highlight
  document.addEventListener("click", function(e) {
    if (e.target.closest(".checkbox")) return;
    if (e.target.tagName === "A" && e.target.closest(".task-title")) return;
    var row = e.target.closest(".task-row");
    if (!row) {
      setTaskFocus(null);
      return;
    }
    var taskItem = row.closest(".task-item");
    if (taskItem) {
      setTaskFocus(taskItem, true);
    }
  });

  // Arrow keys in add-task inputs: navigate between tasks and inputs fluidly
  document.addEventListener("keydown", function(e) {
    if (e.key !== "ArrowUp" && e.key !== "ArrowDown") return;
    var target = e.target;
    if (!target.matches(".task-form input[type='text'], .task-form input[name='title']")) return;

    e.preventDefault();

    // Find the section this input belongs to
    var inputSection = target.closest(".section");
    if (!inputSection) return;

    if (e.key === "ArrowUp") {
      // Up from input: focus the last visible task in this section (or earlier sections)
      var tasks = getVisibleTasks();
      var lastTaskInSection = null;
      for (var i = tasks.length - 1; i >= 0; i--) {
        if (tasks[i].closest(".section") === inputSection) {
          lastTaskInSection = tasks[i];
          break;
        }
      }
      if (lastTaskInSection) {
        target.blur();
        setTaskFocus(lastTaskInSection, true);
      } else {
        // No tasks in this section; find the previous section's input
        var allInputs = Array.from(
          document.querySelectorAll(".task-form input[name='title']")
        ).filter(function(inp) {
          var node = inp.parentElement;
          while (node && node.id !== "center-panel") {
            if (node.tagName === "DETAILS" && !node.open) return false;
            node = node.parentElement;
          }
          return true;
        });
        var currentIdx = allInputs.indexOf(target);
        if (currentIdx > 0) {
          allInputs[currentIdx - 1].focus();
        }
      }
    } else {
      // Down from input: focus the first task in the next section or next section's input
      var allSections = Array.from(document.querySelectorAll("#center-panel .section"));
      var currentSectionIdx = allSections.indexOf(inputSection);
      var tasks = getVisibleTasks();

      // Look for next section
      for (var si = currentSectionIdx + 1; si < allSections.length; si++) {
        var nextSection = allSections[si];
        // Check if section is open (it's a <details> element)
        if (!nextSection.open) continue;

        // Find first task in this section
        var firstTask = null;
        for (var ti = 0; ti < tasks.length; ti++) {
          if (tasks[ti].closest(".section") === nextSection) {
            firstTask = tasks[ti];
            break;
          }
        }
        if (firstTask) {
          target.blur();
          setTaskFocus(firstTask, true);
          return;
        }

        // No tasks in next section -- focus its input
        var nextInput = nextSection.querySelector(".task-form input[name='title']");
        if (nextInput) {
          nextInput.focus();
          return;
        }
      }
    }
  });

  // Ctrl+Left/Right to tab between navigation panels
  document.addEventListener("keydown", function(e) {
    if (!e.ctrlKey) return;
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;

    // Don't intercept when input/textarea/contenteditable is focused
    var tag = e.target.tagName.toLowerCase();
    if (tag === "input" || tag === "textarea" || e.target.isContentEditable) {
      return;
    }

    e.preventDefault();
    var navLinks = Array.from(document.querySelectorAll(".navbar-link"));
    if (navLinks.length === 0) return;

    var activeIdx = -1;
    for (var i = 0; i < navLinks.length; i++) {
      if (navLinks[i].classList.contains("active")) {
        activeIdx = i;
        break;
      }
    }

    var nextIdx;
    if (e.key === "ArrowLeft") {
      nextIdx = activeIdx <= 0 ? navLinks.length - 1 : activeIdx - 1;
    } else {
      nextIdx = activeIdx >= navLinks.length - 1 ? 0 : activeIdx + 1;
    }

    navLinks[nextIdx].click();
  });

  document.addEventListener("keydown", function(e) {
    // Don't intercept when input/textarea/contenteditable is focused
    var tag = e.target.tagName.toLowerCase();
    if (tag === "input" || tag === "textarea" || e.target.isContentEditable) {
      return;
    }

    // Only handle navigation keys
    var navKeys = ["ArrowDown", "ArrowUp", "j", "k", "Tab", "x", "Escape", "Delete"];
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

    // Ctrl+Arrow: jump to next/previous section
    if (e.ctrlKey && (e.key === "ArrowDown" || e.key === "ArrowUp")) {
      e.preventDefault();
      var currentTask = currentIndex >= 0 ? tasks[currentIndex] : null;
      var currentSection = currentTask ? currentTask.closest(".section") : null;

      if (e.key === "ArrowDown") {
        // Find first task in the next section
        var startIdx = currentIndex >= 0 ? currentIndex + 1 : 0;
        for (var i = startIdx; i < tasks.length; i++) {
          var section = tasks[i].closest(".section");
          if (section !== currentSection) {
            setTaskFocus(tasks[i], true);
            return;
          }
        }
        // Wrap to first task
        if (tasks.length > 0) setTaskFocus(tasks[0], true);
      } else {
        // Find first task in the previous section
        var searchIdx = currentIndex >= 0 ? currentIndex - 1 : tasks.length - 1;
        // First, find any task in a previous section
        var prevSection = null;
        for (var i = searchIdx; i >= 0; i--) {
          var section = tasks[i].closest(".section");
          if (section !== currentSection) {
            prevSection = section;
            break;
          }
        }
        if (prevSection) {
          // Jump to the first task in that section
          for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].closest(".section") === prevSection) {
              setTaskFocus(tasks[i], true);
              return;
            }
          }
        }
        // Wrap to last section's first task
        if (tasks.length > 0) {
          var lastSection = tasks[tasks.length - 1].closest(".section");
          for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].closest(".section") === lastSection) {
              setTaskFocus(tasks[i], true);
              return;
            }
          }
        }
      }
      return;
    }

    if (e.key === "ArrowDown" || e.key === "j") {
      e.preventDefault();
      var nextIndex = currentIndex + 1;
      if (nextIndex < tasks.length) {
        // Check if next task is in a different section — if so, go to current section's input first
        var currentTask = currentIndex >= 0 ? tasks[currentIndex] : null;
        var currentSec = currentTask ? currentTask.closest(".section") : null;
        var nextTask = tasks[nextIndex];
        var nextSec = nextTask ? nextTask.closest(".section") : null;

        if (currentSec && nextSec && currentSec !== nextSec) {
          // Focus the add-task input of the current section before moving to next section
          var sectionInput = currentSec.querySelector(".task-form input[name='title']");
          if (sectionInput) {
            setTaskFocus(null);
            sectionInput.focus();
            return;
          }
        }
        setTaskFocus(tasks[nextIndex], true);
      } else {
        // Past the last task — focus the add-task input of the current section
        var currentTask = currentIndex >= 0 ? tasks[currentIndex] : null;
        var currentSec = currentTask ? currentTask.closest(".section") : null;
        if (currentSec) {
          var sectionInput = currentSec.querySelector(".task-form input[name='title']");
          if (sectionInput) {
            setTaskFocus(null);
            sectionInput.focus();
            return;
          }
        }
        setTaskFocus(tasks[0], true);
      }
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

        // Persist silently and update subtask counts
        postMove(focusedTaskId, {
          parent: grandparentId || "null"
        });
        updateSubtaskCounts();
      } else {
        // Indent: move task into previous sibling's subtask drop zone
        // Only indent one level: find the previous sibling at the SAME depth
        // (same parent), not the previous task in the flat list which may be
        // at a deeper level.
        var currentParentId = focused.dataset.parentId || "";

        // Walk backwards through the flat task list to find the previous
        // sibling that shares the same parent (same nesting level).
        var prevSibling = null;
        for (var si = currentIndex - 1; si >= 0; si--) {
          var candidate = tasks[si];
          var candidateParent = candidate.dataset.parentId || "";
          if (candidateParent === currentParentId) {
            prevSibling = candidate;
            break;
          }
        }
        if (!prevSibling) return;

        var prevSiblingId = prevSibling.dataset.taskId;

        // Find the subtask drop zone inside the previous sibling
        var dropZone = prevSibling.querySelector(":scope > .subtask-drop-zone");
        if (!dropZone) {
          // Try inside a details/subtask-collapsible-content wrapper
          var details = prevSibling.querySelector(":scope > .subtask-collapsible");
          if (details) {
            dropZone = details.querySelector(".subtask-drop-zone");
          }
        }
        if (!dropZone) return;

        // Move focused element into the drop zone
        dropZone.appendChild(focused);

        // Update data attribute and visual depth
        focused.dataset.parentId = prevSiblingId;
        var prevDepth = parseInt(prevSibling.style.paddingLeft) || 0;
        focused.style.paddingLeft = (prevDepth + 1) + "em";

        // Persist silently and update subtask counts
        postMove(focusedTaskId, {
          parent: prevSiblingId
        });
        updateSubtaskCounts();
      }
    } else if (e.key === "x" && focusedTaskId) {
      // Quick complete
      var focused = document.querySelector('.task-item[data-task-id="' + focusedTaskId + '"]');
      if (focused) {
        var checkbox = focused.querySelector(".checkbox");
        if (checkbox) checkbox.click();
      }
    } else if (e.key === "Delete" && focusedTaskId) {
      // Delete focused task with confirmation
      e.preventDefault();
      if (!confirm("Delete this task?")) return;

      var taskIdToDelete = focusedTaskId;
      // Move focus to next or previous task before deleting
      var nextIndex = currentIndex + 1 < tasks.length ? currentIndex + 1 : currentIndex - 1;
      if (nextIndex >= 0 && nextIndex < tasks.length && nextIndex !== currentIndex) {
        setTaskFocus(tasks[nextIndex], true);
      } else {
        setTaskFocus(null);
      }

      htmx.ajax("POST", "/tasks/" + taskIdToDelete + "/delete/", {
        target: "#center-panel",
        swap: "innerHTML"
      });
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

// ─── Title Textarea Auto-resize ─────────────

function initTitleInput() {
  var el = document.getElementById("title");
  if (!el || el.tagName !== "TEXTAREA") return;

  function resize() {
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
  }

  el.addEventListener("input", resize);
  resize();

  // Enter submits (triggers change), Shift+Enter does nothing extra
  el.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      el.blur();
    }
  });
}

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

  // Store original value for change detection on blur
  textarea.setAttribute("data-original", textarea.value);

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

  // On blur, deactivate all blocks and trigger save if changed
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
        // Dispatch md-save if content changed
        var original = textarea.getAttribute("data-original") || "";
        if (textarea.value !== original) {
          textarea.setAttribute("data-original", textarea.value);
          editor.dispatchEvent(new CustomEvent("md-save", { bubbles: true }));
        }
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
    }
  });
}

// Click anywhere outside an editing list item saves the edit
document.addEventListener("mousedown", function(e) {
  var editingItem = document.querySelector(".list-nav-item.editing");
  if (!editingItem) return;
  var pickerOpen = emojiPickerEl && emojiPickerEl.style.display !== "none";
  if (editingItem.contains(e.target) || (pickerOpen && emojiPickerEl.contains(e.target))) return;
  var form = editingItem.querySelector(".list-nav-edit-form");
  if (form) {
    htmx.trigger(form, "submit");
  }
});

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

// ─── Section Name Edit ──────────────────────

function initSectionNameEdit() {
  document.querySelectorAll(".section-edit-btn").forEach(function(btn) {
    if (btn._editBound) return;
    btn._editBound = true;

    btn.addEventListener("click", function(e) {
      e.preventDefault();
      var header = btn.closest(".section-header");
      if (!header) return;
      header.classList.add("editing");
      var input = header.querySelector(".section-edit-input");
      if (input) {
        input.focus();
        input.select();
      }
    });
  });

  document.querySelectorAll(".section-edit-cancel").forEach(function(btn) {
    if (btn._cancelBound) return;
    btn._cancelBound = true;

    btn.addEventListener("click", function(e) {
      e.preventDefault();
      var header = btn.closest(".section-header");
      if (header) header.classList.remove("editing");
    });
  });

  document.querySelectorAll(".section-edit-input").forEach(function(input) {
    if (input._keyBound) return;
    input._keyBound = true;

    input.addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        e.preventDefault();
        var form = input.closest(".section-edit-form");
        if (form) htmx.trigger(form, "submit");
      } else if (e.key === "Escape") {
        e.preventDefault();
        var header = input.closest(".section-header");
        if (header) header.classList.remove("editing");
      }
    });
  });
}

// ─── Mobile Panel Toggles ───────────────────

function isMobileOrTablet() {
  return window.innerWidth < 1024;
}

function openSidebar() {
  document.body.classList.add("sidebar-open");
}

function closeSidebar() {
  document.body.classList.remove("sidebar-open");
}

function openDetailPanel() {
  if (isMobileOrTablet()) {
    document.body.classList.add("detail-open");
  }
}

function closeDetailPanel() {
  document.body.classList.remove("detail-open");
}

function initMobilePanels() {
  var hamburger = document.getElementById("sidebar-toggle");
  if (hamburger) {
    hamburger.addEventListener("click", function() {
      if (document.body.classList.contains("sidebar-open")) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  var sidebarBackdrop = document.getElementById("sidebar-backdrop");
  if (sidebarBackdrop) {
    sidebarBackdrop.addEventListener("click", closeSidebar);
  }

  var detailBackdrop = document.getElementById("detail-backdrop");
  if (detailBackdrop) {
    detailBackdrop.addEventListener("click", closeDetailPanel);
  }

  // Bind close button(s) — may exist in detail content or empty state
  document.querySelectorAll(".detail-close-btn").forEach(function(btn) {
    if (btn._closeBound) return;
    btn._closeBound = true;
    btn.addEventListener("click", closeDetailPanel);
  });

  // Close panels on window resize to desktop
  window.addEventListener("resize", function() {
    if (!isMobileOrTablet()) {
      closeSidebar();
      closeDetailPanel();
    }
  });
}

// ─── Active Nav Highlight ───────────────────

function updateActiveNav() {
  var path = window.location.pathname;
  var navMap = {
    "/": "todo",
    "/projects/": "projects",
    "/timesheet/": "timesheet",
    "/import/": "import"
  };

  // Match longest prefix (e.g. /timesheet/?week=-1 → timesheet)
  var active = "";
  for (var prefix in navMap) {
    if (path === prefix || (prefix !== "/" && path.startsWith(prefix))) {
      active = navMap[prefix];
    }
  }
  if (!active && path === "/") active = "todo";

  // Update top navbar links
  document.querySelectorAll(".navbar-link").forEach(function(link) {
    link.classList.remove("active");
    var href = link.getAttribute("href");
    if (navMap[href] === active) link.classList.add("active");
  });

  // Update bottom tab bar
  document.querySelectorAll(".bottom-tab").forEach(function(tab) {
    tab.classList.remove("active");
    var href = tab.getAttribute("href");
    if (navMap[href] === active) tab.classList.add("active");
  });
}

// ─── Task Completion Transitions ─────────────

/**
 * Apply optimistic CSS classes when a checkbox is clicked, providing
 * immediate visual feedback (fade-out) before the server responds.
 * The server returns OOB swaps (hx-swap="none" on the checkbox), so
 * no full center-panel replacement occurs — eliminating the flash.
 */
function initCompletionTransitions() {
  document.body.addEventListener("htmx:beforeRequest", function(e) {
    var elt = e.detail.elt;
    if (!elt || !elt.classList.contains("checkbox")) return;

    var taskItem = elt.closest(".task-item");
    if (!taskItem) return;

    var isCompleting = !elt.classList.contains("checked");
    if (isCompleting) {
      taskItem.classList.add("completing");
    } else {
      taskItem.classList.add("uncompleting");
    }
  });
}

/**
 * Add the intro animation class to sections on initial page load only.
 * Sections inserted later via HTMX swaps won't have this class,
 * so they appear instantly without a fadeInUp flash.
 */
function addSectionIntroAnimation() {
  document.querySelectorAll(".section").forEach(function(el) {
    el.classList.add("section-intro");
  });
}

// ─── Init & HTMX Hooks ──────────────────────

function initAll() {
  try { initSortable(); } catch (ex) { console.error("initSortable error:", ex); }
  setupToastDismiss();
  try { initEmojiPickers(); } catch (ex) { console.error("initEmojiPickers error:", ex); }
  try { initTitleInput(); } catch (ex) { console.error("initTitleInput error:", ex); }
  try { initMarkdownEditor(); } catch (ex) { console.error("initMarkdownEditor error:", ex); }
  try { initListNameEdit(); } catch (ex) { console.error("initListNameEdit error:", ex); }
  try { initSectionNameEdit(); } catch (ex) { console.error("initSectionNameEdit error:", ex); }
  try { initMobilePanels(); } catch (ex) { console.error("initMobilePanels error:", ex); }
  updateSubtaskCounts();
  restoreTaskFocus();
  restoreFocus();
}

// Re-init after HTMX swaps.
// We listen on both htmx:afterSwap AND htmx:afterSettle.
//   - afterSwap catches the main swap and fires initAll() immediately.
//   - afterSettle fires once the settle phase completes (after OOB
//     swaps have been applied), so we re-run initAll() to pick up
//     any sidebar DOM that was replaced out-of-band.
// The double call is harmless because initAll() calls
// destroySortables() first, and the second pass simply re-binds on
// the final DOM.  This ensures Sortable instances are never left on
// stale (replaced) elements.
document.addEventListener("htmx:afterSwap", function(e) {
  initAll();
  // Close sidebar when center panel swaps (user selected a list)
  if (e.detail.target && e.detail.target.id === "center-panel") {
    closeSidebar();
  }
  // Close both panels when page-body swaps (navbar navigation)
  if (e.detail.target && e.detail.target.id === "page-body") {
    closeSidebar();
    closeDetailPanel();
    updateActiveNav();
  }
});
document.addEventListener("htmx:afterSettle", function(e) {
  initAll();
});

// Init on page load
document.addEventListener("DOMContentLoaded", function() {
  trackFormFocus();
  initKeyboardNav();
  initCompletionTransitions();
  addSectionIntroAnimation();
  initAll();

  // Register service worker for PWA support
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/service-worker.js");
  }
});
