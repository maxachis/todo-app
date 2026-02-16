/* ============================================
   Mobile Panels, Nav Highlight, Sidebar/Section Editing
   ============================================ */

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

  document.querySelectorAll(".detail-close-btn").forEach(function(btn) {
    if (btn._closeBound) return;
    btn._closeBound = true;
    btn.addEventListener("click", closeDetailPanel);
  });

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

  var active = "";
  for (var prefix in navMap) {
    if (path === prefix || (prefix !== "/" && path.startsWith(prefix))) {
      active = navMap[prefix];
    }
  }
  if (!active && path === "/") active = "todo";

  document.querySelectorAll(".navbar-link").forEach(function(link) {
    link.classList.remove("active");
    var href = link.getAttribute("href");
    if (navMap[href] === active) link.classList.add("active");
  });

  document.querySelectorAll(".bottom-tab").forEach(function(tab) {
    tab.classList.remove("active");
    var href = tab.getAttribute("href");
    if (navMap[href] === active) tab.classList.add("active");
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

    display.addEventListener("dblclick", function(e) {
      e.preventDefault();
      e.stopPropagation();
      li.classList.add("editing");
      if (nameInput) {
        nameInput.focus();
        nameInput.select();
      }
    });

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
  var pickerOpen = emojiPickerEl && emojiPickerEl.style.display !== "none";

  if (editingItem && !editingItem.contains(e.target) && !(pickerOpen && emojiPickerEl.contains(e.target))) {
    var form = editingItem.querySelector(".list-nav-edit-form");
    if (form) {
      htmx.trigger(form, "submit");
    }
  }

  var listHeader = document.querySelector(".list-header-left.editing");
  if (listHeader && !listHeader.contains(e.target) && !(pickerOpen && emojiPickerEl.contains(e.target))) {
    var headerForm = listHeader.querySelector(".list-header-edit-form");
    if (headerForm) {
      htmx.trigger(headerForm, "submit");
    }
  }
});

function cancelEdit(li) {
  li.classList.remove("editing");
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

function initListHeaderEdit() {
  var headerLeft = document.querySelector(".list-header-left");
  if (!headerLeft || headerLeft._editBound) return;
  headerLeft._editBound = true;

  var display = headerLeft.querySelector("[data-list-header-display]");
  var title = headerLeft.querySelector("[data-list-header-title]");
  var editForm = headerLeft.querySelector(".list-header-edit-form");
  var cancelBtn = headerLeft.querySelector(".list-header-edit-cancel");
  var nameInput = editForm ? editForm.querySelector('input[name="name"]') : null;
  var displayEmoji = display ? display.querySelector(".list-header-emoji") : null;
  var emojiInput = editForm ? editForm.querySelector('input[name="emoji"]') : null;
  var formEmojiBtn = editForm ? editForm.querySelector(".emoji-trigger") : null;

  function openHeaderEdit() {
    headerLeft.classList.add("editing");
    if (nameInput) {
      nameInput.focus();
      nameInput.select();
    }
  }

  function cancelHeaderEdit() {
    headerLeft.classList.remove("editing");
    if (title && nameInput) {
      nameInput.value = title.textContent.trim();
    }
    if (displayEmoji && emojiInput) {
      var emoji = displayEmoji.textContent.trim();
      emojiInput.value = emoji;
      if (formEmojiBtn) formEmojiBtn.textContent = emoji || "+";
    }
  }

  if (display) {
    display.addEventListener("click", function(e) {
      e.preventDefault();
      e.stopPropagation();
      openHeaderEdit();
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener("click", function(e) {
      e.preventDefault();
      cancelHeaderEdit();
    });
  }

  if (nameInput) {
    nameInput.addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        e.preventDefault();
        htmx.trigger(editForm, "submit");
      } else if (e.key === "Escape") {
        e.preventDefault();
        cancelHeaderEdit();
      }
    });
  }
}

function initPinButtons() {
  // No-op — pin buttons use hx-post directly, no extra JS needed.
}

// Toggle pin button appearance when server confirms pin/unpin.
document.addEventListener("pinToggled", function(e) {
  var detail = e.detail || {};
  var taskId = detail.taskId;
  var pinned = detail.pinned;
  if (!taskId) return;

  // Find all pin buttons for this task (may appear in section + pinned area)
  document.querySelectorAll('.pin-btn[data-pin-task-id="' + taskId + '"]').forEach(function(btn) {
    var svg = btn.querySelector("svg path:last-child");
    if (pinned) {
      btn.classList.add("pinned");
      btn.title = "Unpin";
      if (svg) svg.setAttribute("fill", "currentColor");
    } else {
      btn.classList.remove("pinned");
      btn.title = "Pin to top";
      if (svg) svg.setAttribute("fill", "none");
    }
  });
});

function jumpToTask(taskId) {
  var target = document.getElementById("task-" + taskId);
  if (!target) return;

  var section = target.closest(".section");
  if (section && !section.open) {
    section.setAttribute("open", "");
  }
  var subtaskWrapper = target.closest(".subtask-collapsible");
  if (subtaskWrapper && !subtaskWrapper.open) {
    subtaskWrapper.setAttribute("open", "");
  }

  target.scrollIntoView({ behavior: "smooth", block: "center" });
  target.classList.add("pin-target-flash");
  setTimeout(function() {
    target.classList.remove("pin-target-flash");
  }, 1000);
}


// ─── Toggle All Sections ────────────────────

function toggleAllSections() {
  var sections = document.querySelectorAll("#center-panel .section");
  var btn = document.getElementById("toggle-all-sections");
  var anyOpen = false;
  sections.forEach(function(s) { if (s.open) anyOpen = true; });

  sections.forEach(function(s) {
    if (anyOpen) {
      s.removeAttribute("open");
    } else {
      s.setAttribute("open", "");
    }
  });

  if (btn) {
    btn.textContent = anyOpen ? "Expand All" : "Collapse All";
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
