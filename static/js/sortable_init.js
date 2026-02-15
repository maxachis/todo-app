/* ============================================
   SortableJS Initialization — Targeted
   Uses a WeakMap to track which DOM elements already
   have Sortable instances, avoiding wasteful global
   destroy+rebuild on every HTMX swap.
   ============================================ */

var sortableMap = new WeakMap();

/**
 * Destroy Sortable instance on a specific element if one exists.
 */
function destroySortableOn(el) {
  var instance = sortableMap.get(el);
  if (instance) {
    try { instance.destroy(); } catch (ex) { /* element may be detached */ }
    sortableMap.delete(el);
  }
}

/**
 * Create a Sortable on `el` only if it doesn't already have one.
 * Returns the instance (new or existing).
 */
function ensureSortable(el, options) {
  if (sortableMap.has(el)) return sortableMap.get(el);
  var instance = new Sortable(el, options);
  sortableMap.set(el, instance);
  return instance;
}

function initSortable() {
  document.querySelectorAll(".sortable-tasks").forEach(function(el) {
    ensureSortable(el, {
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

        evt.item.dataset.parentId = newParentId === "null" ? "" : newParentId;
        evt.item.dataset.sectionId = newSectionId;

        postMove(taskId, {
          section: newSectionId,
          position: newIndex * 10,
          parent: newParentId
        });
      }
    });
  });

  // Sidebar list drop targets for cross-list moves
  document.querySelectorAll(".list-nav-item").forEach(function(el) {
    ensureSortable(el, {
      group: {
        name: "tasks",
        put: function(to, from, dragEl) {
          // Only accept actual task items, not list nav items being reordered
          return !!dragEl.dataset.taskId;
        },
        pull: false
      },
      sort: false,
      onAdd: function(evt) {
        var taskId = evt.item.dataset.taskId;
        var listId = evt.to.dataset.listId;

        if (!taskId) {
          // Not a task drop — a list nav item was moved here by mistake.
          // Return it to its original container.
          if (evt.from && evt.from !== evt.to) {
            evt.from.insertBefore(evt.item, evt.from.children[evt.oldIndex] || null);
          }
          return;
        }

        htmx.ajax("POST", "/tasks/" + taskId + "/move/", {
          values: {
            list: listId,
            csrfmiddlewaretoken: getCsrfToken()
          },
          swap: "none"
        });
      }
    });
  });

  // Section reordering within a list
  document.querySelectorAll(".sortable-sections").forEach(function(el) {
    var sectionDragClickBlocker = null;

    ensureSortable(el, {
      animation: 150,
      ghostClass: "sortable-ghost",
      chosenClass: "sortable-chosen",
      handle: ".section-header",
      draggable: ".section",
      onStart: function(evt) {
        sectionDragClickBlocker = function(e) { e.preventDefault(); };
        evt.item.addEventListener("click", sectionDragClickBlocker, true);
      },
      onEnd: function(evt) {
        var item = evt.item;
        setTimeout(function() {
          if (sectionDragClickBlocker) {
            item.removeEventListener("click", sectionDragClickBlocker, true);
            sectionDragClickBlocker = null;
          }
        }, 50);

        var sectionEl = evt.item;
        var sectionId = sectionEl.dataset.sectionId;
        var newIndex = typeof evt.newDraggableIndex === "number"
          ? evt.newDraggableIndex : evt.newIndex;

        postSectionMove(sectionId, {
          position: newIndex * 10
        });
      }
    });
  });

  // List reordering in the sidebar
  var listNav = document.getElementById("list-nav");
  if (listNav) {
    ensureSortable(listNav, {
      animation: 150,
      ghostClass: "sortable-ghost",
      chosenClass: "sortable-chosen",
      handle: ".list-drag-handle",
      draggable: ".list-nav-item",
      onEnd: function(evt) {
        var listItem = evt.item;
        var listId = listItem.dataset.listId;
        var newIndex = typeof evt.newDraggableIndex === "number"
          ? evt.newDraggableIndex : evt.newIndex;

        postListMove(listId, {
          position: newIndex * 10
        });
      }
    });
  }
}

// Clean up Sortable instances on elements about to be replaced by HTMX
document.addEventListener("htmx:beforeSwap", function(e) {
  var target = e.detail.target;
  if (!target) return;
  // Destroy sortables on all sortable elements within the swap target
  target.querySelectorAll(".sortable-tasks, .sortable-sections, .list-nav-item").forEach(function(el) {
    destroySortableOn(el);
  });
  // Also check if the target itself is sortable
  destroySortableOn(target);
  // Handle #list-nav specifically
  var listNav = target.querySelector("#list-nav");
  if (listNav) destroySortableOn(listNav);
  if (target.id === "list-nav") destroySortableOn(target);
});
