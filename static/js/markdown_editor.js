/* ============================================
   Title Textarea Auto-resize & Markdown Live Editor
   ============================================ */

function initTitleInput() {
  var el = document.getElementById("title");
  if (!el || el.tagName !== "TEXTAREA") return;

  function resize() {
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
  }

  el.addEventListener("input", resize);
  resize();

  el.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      el.blur();
    }
  });
}

function initMarkdownEditor() {
  var editor = document.getElementById("md-editor");
  var textarea = document.getElementById("notes");
  if (!editor || !textarea) return;

  var isRendering = false;
  var activeBlockIndex = -1;

  function parseBlocks(text) {
    if (!text) return [{ type: "p", raw: "" }];
    var lines = text.split("\n");
    var blocks = [];
    var i = 0;

    while (i < lines.length) {
      var line = lines[i];

      if (line.match(/^```/)) {
        var lang = line.slice(3).trim();
        var codeLines = [];
        i++;
        while (i < lines.length && !lines[i].match(/^```/)) {
          codeLines.push(lines[i]);
          i++;
        }
        i++;
        blocks.push({ type: "code", raw: "```" + lang + "\n" + codeLines.join("\n") + "\n```", content: codeLines.join("\n"), lang: lang });
        continue;
      }

      var headingMatch = line.match(/^(#{1,3})\s+(.*)/);
      if (headingMatch) {
        blocks.push({ type: "h" + headingMatch[1].length, raw: line, content: headingMatch[2] });
        i++;
        continue;
      }

      if (line.match(/^(---|\*\*\*|___)\s*$/)) {
        blocks.push({ type: "hr", raw: line });
        i++;
        continue;
      }

      if (line.match(/^>\s?/)) {
        var quoteLines = [];
        while (i < lines.length && lines[i].match(/^>\s?/)) {
          quoteLines.push(lines[i].replace(/^>\s?/, ""));
          i++;
        }
        blocks.push({ type: "blockquote", raw: quoteLines.map(function(l) { return "> " + l; }).join("\n"), content: quoteLines.join("\n") });
        continue;
      }

      if (line.match(/^[\-\*]\s/)) {
        var listLines = [];
        while (i < lines.length && lines[i].match(/^[\-\*]\s/)) {
          listLines.push(lines[i].replace(/^[\-\*]\s/, ""));
          i++;
        }
        blocks.push({ type: "ul", raw: listLines.map(function(l) { return "- " + l; }).join("\n"), items: listLines });
        continue;
      }

      if (line.match(/^\d+\.\s/)) {
        var listLines = [];
        while (i < lines.length && lines[i].match(/^\d+\.\s/)) {
          listLines.push(lines[i].replace(/^\d+\.\s/, ""));
          i++;
        }
        blocks.push({ type: "ol", raw: listLines.map(function(l, idx) { return (idx + 1) + ". " + l; }).join("\n"), items: listLines });
        continue;
      }

      if (line.trim() === "") {
        i++;
        continue;
      }

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

  function renderInline(text) {
    if (!text) return "";
    var html = text;
    html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/__(.+?)__/g, "<strong>$1</strong>");
    html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");
    html = html.replace(/_(.+?)_/g, "<em>$1</em>");
    html = html.replace(/~~(.+?)~~/g, "<del>$1</del>");
    html = html.replace(/`(.+?)`/g, "<code>$1</code>");
    html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    return html;
  }

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

  function renderEditor(blocks, activeIdx) {
    isRendering = true;
    var html = "";
    blocks.forEach(function(block, idx) {
      if (idx === activeIdx) {
        var rawEscaped = (block.raw || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        html += '<div class="md-block md-block-active" data-block-idx="' + idx + '">' + rawEscaped + '</div>';
      } else {
        html += '<div class="md-block" data-block-idx="' + idx + '">' + renderBlock(block) + '</div>';
      }
    });

    var sel = window.getSelection();
    var cursorOffset = 0;
    if (sel.rangeCount > 0 && editor.contains(sel.anchorNode)) {
      cursorOffset = sel.anchorOffset;
    }

    editor.innerHTML = html;

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

  function getEditorText() {
    var blocks = editor.querySelectorAll(".md-block");
    var parts = [];
    blocks.forEach(function(blockEl) {
      var idx = parseInt(blockEl.dataset.blockIdx);
      if (blockEl.classList.contains("md-block-active")) {
        parts.push(blockEl.textContent);
      } else {
        parts.push(currentBlocks[idx] ? currentBlocks[idx].raw : blockEl.textContent);
      }
    });
    return parts.join("\n\n");
  }

  var currentBlocks = parseBlocks(textarea.value);

  textarea.setAttribute("data-original", textarea.value);

  renderEditor(currentBlocks, -1);

  document.addEventListener("selectionchange", function() {
    if (isRendering) return;
    if (!editor.contains(document.activeElement) && document.activeElement !== editor) return;

    var sel = window.getSelection();
    if (!sel.rangeCount) return;

    var node = sel.anchorNode;
    var blockEl = null;

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
        if (activeBlockIndex >= 0) {
          var oldActive = editor.querySelector('.md-block-active');
          if (oldActive && currentBlocks[activeBlockIndex]) {
            currentBlocks[activeBlockIndex].raw = oldActive.textContent;
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

  editor.addEventListener("input", function() {
    if (isRendering) return;
    textarea.value = getEditorText();
  });

  editor.addEventListener("paste", function(e) {
    e.preventDefault();
    var text = e.clipboardData.getData("text/plain");
    document.execCommand("insertText", false, text);
  });

  editor.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();

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

      var newBlock = { type: "p", raw: "", content: "" };
      var insertIdx = activeBlockIndex >= 0 ? activeBlockIndex + 1 : currentBlocks.length;
      currentBlocks.splice(insertIdx, 0, newBlock);
      activeBlockIndex = insertIdx;

      renderEditor(currentBlocks, activeBlockIndex);
      textarea.value = getEditorText();

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

  document.addEventListener("htmx:configRequest", function(e) {
    if (e.detail.elt.closest && e.detail.elt.closest("form") === editor.closest("form")) {
      if (activeBlockIndex >= 0) {
        var activeEl = editor.querySelector('.md-block-active');
        if (activeEl && currentBlocks[activeBlockIndex]) {
          currentBlocks[activeBlockIndex].raw = activeEl.textContent;
        }
      }
      textarea.value = getEditorText();
    }
  });

  editor.addEventListener("blur", function() {
    if (isRendering) return;
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
    setTimeout(function() {
      if (document.activeElement !== editor && !editor.contains(document.activeElement)) {
        renderEditor(currentBlocks, -1);
        textarea.value = getEditorText();
        var original = textarea.getAttribute("data-original") || "";
        if (textarea.value !== original) {
          textarea.setAttribute("data-original", textarea.value);
          editor.dispatchEvent(new CustomEvent("md-save", { bubbles: true }));
        }
      }
    }, 100);
  });
}
