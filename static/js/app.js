function dismissToast() {
  var toast = document.getElementById("undo-toast");
  if (toast) {
    toast.remove();
  }
}

function initSortable() {
  document.querySelectorAll(".sortable-tasks").forEach(function(el) {
    if (el._sortable) return;
    el._sortable = new Sortable(el, {
      group: "tasks",
      animation: 150,
      ghostClass: "sortable-ghost",
      chosenClass: "sortable-chosen",
      handle: ".task-row",
      onEnd: function(evt) {
        var taskId = evt.item.dataset.taskId;
        var newSectionId = evt.to.dataset.sectionId;
        var newIndex = evt.newIndex;

        var formData = new FormData();
        formData.append("section", newSectionId);
        formData.append("position", newIndex * 10);

        htmx.ajax("POST", "/tasks/" + taskId + "/move/", {
          values: {
            section: newSectionId,
            position: newIndex * 10,
            csrfmiddlewaretoken: getCsrfToken()
          },
          target: "#center-panel",
          swap: "innerHTML"
        });
      }
    });
  });

  // Sidebar list drop targets for cross-list moves
  document.querySelectorAll(".list-nav-item").forEach(function(el) {
    if (el._sortable) return;
    el._sortable = new Sortable(el, {
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
  });
}

function getCsrfToken() {
  var cookie = document.cookie.split(";").find(function(c) {
    return c.trim().startsWith("csrftoken=");
  });
  return cookie ? cookie.split("=")[1] : "";
}

// Auto-dismiss toasts with fade-out animation
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

// Re-init after HTMX swaps
document.addEventListener("htmx:afterSwap", function() {
  initSortable();
  setupToastDismiss();
});

// Init on page load
document.addEventListener("DOMContentLoaded", function() {
  initSortable();
  setupToastDismiss();
});
