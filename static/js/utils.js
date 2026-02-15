/* ============================================
   Shared Utilities
   ============================================ */

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

    var activeCount = dropZone.querySelectorAll(":scope > .task-item:not(.completed)").length;
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
