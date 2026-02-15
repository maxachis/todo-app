/* ============================================
   Task Completion Transitions
   ============================================ */

/**
 * CSS transition duration in ms — must match the value in style.css
 * for `.task-item.completing` and `.task-item.uncompleting`.
 */
var COMPLETION_TRANSITION_MS = 180;

/**
 * Apply optimistic CSS classes when a checkbox is clicked, providing
 * immediate visual feedback (fade-out) before the server responds.
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

  /* Listen for the custom HX-Trigger events from the server. */
  document.body.addEventListener("taskCompleted", function(e) {
    var detail = e.detail || {};
    var taskId = detail.taskId;
    if (!taskId) return;
    _handleTaskCompleted(taskId, detail.parentId);
  });

  document.body.addEventListener("taskUncompleted", function(e) {
    var detail = e.detail || {};
    var taskId = detail.taskId;
    if (!taskId) return;
    _handleTaskUncompleted(taskId, detail.parentId);
  });
}

/**
 * Handle task completion: wait for CSS transition, then move the task
 * DOM element from the active list into the completed group.
 */
function _handleTaskCompleted(taskId, parentId) {
  var taskEl = document.getElementById("task-" + taskId);
  if (!taskEl) return;

  /* Determine how long to wait — if the transition already started
     (via the htmx:beforeRequest handler), wait for it to finish.
     Otherwise apply it now and wait. */
  if (!taskEl.classList.contains("completing")) {
    taskEl.classList.add("completing");
  }

  setTimeout(function() {
    _moveTaskToCompleted(taskEl, parentId);
    updateSubtaskCounts();
  }, COMPLETION_TRANSITION_MS);
}

/**
 * Handle task uncompletion: wait for CSS transition, then move the
 * task DOM element from the completed group back to the active list.
 */
function _handleTaskUncompleted(taskId, parentId) {
  var taskEl = document.getElementById("task-" + taskId);
  if (!taskEl) return;

  if (!taskEl.classList.contains("uncompleting")) {
    taskEl.classList.add("uncompleting");
  }

  setTimeout(function() {
    _moveTaskToActive(taskEl, parentId);
    updateSubtaskCounts();
  }, COMPLETION_TRANSITION_MS);
}

/**
 * Mark a single task element as completed in the DOM: update classes,
 * checkbox state, and hx-post URL. Does NOT move the element.
 */
function _markElementCompleted(el) {
  el.classList.remove("completing");
  el.classList.add("completed");

  var cb = el.querySelector(":scope > .task-row > .checkbox");
  if (cb) {
    cb.classList.add("checked");
    cb.setAttribute("hx-post", "/tasks/" + el.dataset.taskId + "/uncomplete/");
    cb.innerHTML = "&#9745;";
    htmx.process(cb);
  }
}

/**
 * Move a task element into the completed group and update its markup
 * to reflect the completed state (checkbox, class, etc.).
 * Also cascades visual completion to all nested subtask elements.
 */
function _moveTaskToCompleted(taskEl, parentId) {
  /* Mark the parent task element as completed */
  _markElementCompleted(taskEl);

  /* Cascade: mark all nested subtask elements as completed too */
  var subtaskEls = taskEl.querySelectorAll(".task-item:not(.completed)");
  subtaskEls.forEach(function(subEl) {
    _markElementCompleted(subEl);
  });

  /* Find the correct completed group to move into */
  var completedContainer;
  if (parentId) {
    /* This is a subtask — find the parent's subtask-completed-group */
    var parentEl = document.getElementById("task-" + parentId);
    if (parentEl) {
      completedContainer = parentEl.querySelector(
        ":scope > .subtask-collapsible > .subtask-collapsible-content > .subtask-completed-group > .subtask-completed-items"
      );
    }
  } else {
    /* This is a top-level task — find the section's completed group */
    var sectionId = taskEl.dataset.sectionId;
    var sectionEl = document.getElementById("section-" + sectionId);
    if (sectionEl) {
      completedContainer = sectionEl.querySelector(
        ":scope > .completed-group > .completed-group-items"
      );
    }
  }

  if (completedContainer) {
    completedContainer.appendChild(taskEl);
  }
}

/**
 * Move a task element from the completed group back to the active
 * task list and update its markup to reflect the active state.
 */
function _moveTaskToActive(taskEl, parentId) {
  /* Update task element state — only this task, not its subtasks */
  taskEl.classList.remove("uncompleting", "completed");

  /* Update checkbox: unchecked state + hx-post URL */
  var checkbox = taskEl.querySelector(":scope > .task-row > .checkbox");
  if (checkbox) {
    checkbox.classList.remove("checked");
    var taskId = taskEl.dataset.taskId;
    checkbox.setAttribute("hx-post", "/tasks/" + taskId + "/complete/");
    checkbox.innerHTML = "&#9744;";
    htmx.process(checkbox);
  }

  /* Find the correct active list to move into */
  var activeContainer;
  if (parentId) {
    /* This is a subtask — find the parent's subtask-drop-zone */
    var parentEl = document.getElementById("task-" + parentId);
    if (parentEl) {
      activeContainer = parentEl.querySelector(
        ":scope > .subtask-collapsible > .subtask-collapsible-content > .subtask-drop-zone"
      );
    }
  } else {
    /* This is a top-level task — find the section's task-list */
    var sectionId = taskEl.dataset.sectionId;
    var sectionEl = document.getElementById("section-" + sectionId);
    if (sectionEl) {
      activeContainer = sectionEl.querySelector(":scope > .task-list");
    }
  }

  if (activeContainer) {
    activeContainer.appendChild(taskEl);
  }
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
