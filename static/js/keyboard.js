/* ============================================
   Keyboard Navigation
   ============================================ */

var focusedTaskId = null;
var _suppressTaskFocusRestore = false;

function suppressTaskFocusRestore() {
  _suppressTaskFocusRestore = true;
  focusedTaskId = null;
  document.querySelectorAll(".task-row.keyboard-focus").forEach(function(el) {
    el.classList.remove("keyboard-focus");
  });
}

function getVisibleTasks() {
  return Array.from(
    document.querySelectorAll("#center-panel .task-item:not(.completed)")
  ).filter(function(el) {
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
  document.querySelectorAll(".task-row.keyboard-focus").forEach(function(el) {
    el.classList.remove("keyboard-focus");
  });
  if (taskEl) {
    var row = taskEl.querySelector(":scope > .task-row");
    if (row) {
      row.classList.add("keyboard-focus");
    }
    focusedTaskId = taskEl.dataset.taskId;
    taskEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
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
  if (_suppressTaskFocusRestore) {
    _suppressTaskFocusRestore = false;
    return;
  }
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

  // Click on a task row -> highlight + load detail (skip checkbox clicks)
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

  // Arrow keys in add-task inputs
  document.addEventListener("keydown", function(e) {
    if (e.key !== "ArrowUp" && e.key !== "ArrowDown") return;
    var target = e.target;
    if (!target.matches(".task-form input[type='text'], .task-form input[name='title']")) return;

    e.preventDefault();

    var inputSection = target.closest(".section");
    if (!inputSection) return;

    if (e.key === "ArrowUp") {
      var tasks = getVisibleTasks();
      var lastTaskInSection = null;
      for (var i = tasks.length - 1; i >= 0; i--) {
        if (tasks[i].closest(".section") === inputSection) {
          lastTaskInSection = tasks[i];
          break;
        }
      }
      if (lastTaskInSection) {
        lastFocusedInputSelector = null;
        suppressRestoreFocus();
        target.blur();
        setTaskFocus(lastTaskInSection, true);
      } else {
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
      var allSections = Array.from(document.querySelectorAll("#center-panel .section"));
      var currentSectionIdx = allSections.indexOf(inputSection);
      var tasks = getVisibleTasks();

      for (var si = currentSectionIdx + 1; si < allSections.length; si++) {
        var nextSection = allSections[si];
        if (!nextSection.open) continue;

        var firstTask = null;
        for (var ti = 0; ti < tasks.length; ti++) {
          if (tasks[ti].closest(".section") === nextSection) {
            firstTask = tasks[ti];
            break;
          }
        }
        if (firstTask) {
          lastFocusedInputSelector = null;
          suppressRestoreFocus();
          target.blur();
          setTaskFocus(firstTask, true);
          return;
        }

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
    var tag = e.target.tagName.toLowerCase();
    if (tag === "input" || tag === "textarea" || e.target.isContentEditable) {
      return;
    }

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
        var startIdx = currentIndex >= 0 ? currentIndex + 1 : 0;
        for (var i = startIdx; i < tasks.length; i++) {
          var section = tasks[i].closest(".section");
          if (section !== currentSection) {
            setTaskFocus(tasks[i], true);
            return;
          }
        }
        if (tasks.length > 0) setTaskFocus(tasks[0], true);
      } else {
        var searchIdx = currentIndex >= 0 ? currentIndex - 1 : tasks.length - 1;
        var prevSection = null;
        for (var i = searchIdx; i >= 0; i--) {
          var section = tasks[i].closest(".section");
          if (section !== currentSection) {
            prevSection = section;
            break;
          }
        }
        if (prevSection) {
          for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].closest(".section") === prevSection) {
              setTaskFocus(tasks[i], true);
              return;
            }
          }
        }
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
        var currentTask = currentIndex >= 0 ? tasks[currentIndex] : null;
        var currentSec = currentTask ? currentTask.closest(".section") : null;
        var nextTask = tasks[nextIndex];
        var nextSec = nextTask ? nextTask.closest(".section") : null;

        if (currentSec && nextSec && currentSec !== nextSec) {
          var sectionInput = currentSec.querySelector(".task-form input[name='title']");
          if (sectionInput) {
            setTaskFocus(null);
            sectionInput.focus();
            return;
          }
        }
        setTaskFocus(tasks[nextIndex], true);
      } else {
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
        // Outdent
        var currentParentId = focused.dataset.parentId;
        if (!currentParentId) return;

        var parentEl = document.querySelector('.task-item[data-task-id="' + currentParentId + '"]');
        if (!parentEl) return;

        var grandparentId = parentEl.dataset.parentId || "";
        var targetContainer = parentEl.parentNode;

        if (parentEl.nextSibling) {
          targetContainer.insertBefore(focused, parentEl.nextSibling);
        } else {
          targetContainer.appendChild(focused);
        }

        focused.dataset.parentId = grandparentId;
        var parentDepth = parseInt(parentEl.style.paddingLeft) || 0;
        focused.style.paddingLeft = parentDepth + "em";

        postMove(focusedTaskId, {
          parent: grandparentId || "null"
        });
        updateSubtaskCounts();
      } else {
        // Indent
        var currentParentId = focused.dataset.parentId || "";

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

        var dropZone = prevSibling.querySelector(":scope > .subtask-drop-zone");
        if (!dropZone) {
          var details = prevSibling.querySelector(":scope > .subtask-collapsible");
          if (details) {
            dropZone = details.querySelector(".subtask-drop-zone");
          }
        }
        if (!dropZone) return;

        dropZone.appendChild(focused);

        focused.dataset.parentId = prevSiblingId;
        var prevDepth = parseInt(prevSibling.style.paddingLeft) || 0;
        focused.style.paddingLeft = (prevDepth + 1) + "em";

        postMove(focusedTaskId, {
          parent: prevSiblingId
        });
        updateSubtaskCounts();
      }
    } else if (e.key === "x" && focusedTaskId) {
      var focused = document.querySelector('.task-item[data-task-id="' + focusedTaskId + '"]');
      if (focused) {
        var checkbox = focused.querySelector(".checkbox");
        if (checkbox) checkbox.click();
      }
    } else if (e.key === "Delete" && focusedTaskId) {
      e.preventDefault();
      if (!confirm("Delete this task?")) return;

      var taskIdToDelete = focusedTaskId;
      var nextIndex = currentIndex + 1 < tasks.length ? currentIndex + 1 : currentIndex - 1;
      if (nextIndex >= 0 && nextIndex < tasks.length && nextIndex !== currentIndex) {
        setTaskFocus(tasks[nextIndex], true);
      } else {
        setTaskFocus(null);
      }

      htmx.ajax("POST", "/tasks/" + taskIdToDelete + "/delete/", {
        swap: "none"
      });
    } else if (e.key === "Escape") {
      setTaskFocus(null);
    }
  });
}
