/* ═══════════════════════════════════════════════════════════════════
   Edugator – script.js
   Handles: chat logic, API calls, UI rendering, sidebar, modal
═══════════════════════════════════════════════════════════════════ */

"use strict";

// ─── DOM REFERENCES ──────────────────────────────────────────────────────────
const chatContainer   = document.getElementById("chatContainer");
const chatMessages    = document.getElementById("chatMessages");
const welcomeScreen   = document.getElementById("welcomeScreen");
const userInput       = document.getElementById("userInput");
const sendBtn         = document.getElementById("sendBtn");
const clearChatBtn    = document.getElementById("clearChat");
const menuBtn         = document.getElementById("menuBtn");
const sidebar         = document.getElementById("sidebar");
const sidebarClose    = document.getElementById("sidebarClose");
const sidebarOverlay  = document.getElementById("sidebarOverlay");
const categoryList    = document.getElementById("categoryList");
const suggestionList  = document.getElementById("suggestionList");
const modalOverlay    = document.getElementById("modalOverlay");
const modalClose      = document.getElementById("modalClose");
const modalBody       = document.getElementById("modalBody");

// ─── STATE ───────────────────────────────────────────────────────────────────
let conversationHistory = [];   // { role: "user"|"bot", content: "..." }
let isLoading           = false;
let typingRow           = null; // DOM node for the typing indicator

// ─── CATEGORY QUERY MAP ───────────────────────────────────────────────────────
// Maps category IDs → a prompt that gets sent when the user clicks a category button
const CATEGORY_QUERIES = {
  after10: "What are the stream options available after 10th grade in India? Explain Science, Commerce, Arts, Polytechnic, and ITI options.",
  after12: "What are all the course and career options available after 12th grade in India? Cover engineering, medical, arts & science, and commerce paths.",
  career:  "Give me a complete overview of career options in India — IT, government jobs, banking, teaching, and entrepreneurship.",
  exams:   "List and explain all the major entrance and competitive exams in India — JEE, NEET, UPSC, SSC, Banking, TNPSC, TNEA, and others.",
  govt:    "How can I get a government job in India after graduation? Explain UPSC, SSC, TNPSC, banking exams, and the step-by-step process.",
  skills:  "What technical and soft skills do I need to get a job in the IT industry in India? Give me a complete roadmap.",
};

// ─── INIT ─────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  loadCategories();
  loadSuggestions();
  autoResizeTextarea();
  setupEventListeners();
});

// ─── EVENT LISTENERS ─────────────────────────────────────────────────────────
function setupEventListeners() {

  // Send on Enter (Shift+Enter = new line)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });

  // Send button click
  sendBtn.addEventListener("click", handleSend);

  // Clear chat
  clearChatBtn.addEventListener("click", clearChat);

  // Sidebar open/close (mobile)
  menuBtn.addEventListener("click",         openSidebar);
  sidebarClose.addEventListener("click",    closeSidebar);
  sidebarOverlay.addEventListener("click",  closeSidebar);

  // Source modal close
  modalClose.addEventListener("click",      closeModal);
  modalOverlay.addEventListener("click", (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  // Welcome screen cards → fire that question
  document.querySelectorAll(".welcome-card").forEach((card) => {
    card.addEventListener("click", () => {
      const query = card.dataset.query;
      if (query) sendMessage(query);
    });
  });

  // Auto-resize textarea as user types
  userInput.addEventListener("input", () => {
    autoResizeTextarea();
    updateSendBtn();
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
//  LOAD SIDEBAR DATA
// ═══════════════════════════════════════════════════════════════════════════════

async function loadCategories() {
  try {
    const res  = await fetch("/api/categories");
    const data = await res.json();

    categoryList.innerHTML = "";

    data.categories.forEach((cat) => {
      const btn = document.createElement("button");
      btn.className    = "cat-btn";
      btn.dataset.id   = cat.id;
      btn.innerHTML    = `<span class="cat-icon">${cat.icon}</span>${cat.label}`;
      btn.style.setProperty("--cat-color", cat.color);

      btn.addEventListener("click", () => {
        // Toggle active state
        document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        const query = CATEGORY_QUERIES[cat.id];
        if (query) {
          closeSidebar();
          sendMessage(query);
        }
      });

      categoryList.appendChild(btn);
    });
  } catch (err) {
    console.warn("Could not load categories:", err);
    categoryList.innerHTML = `<p style="font-size:0.78rem;color:var(--text2);padding:4px">Could not load categories.</p>`;
  }
}

async function loadSuggestions() {
  try {
    const res  = await fetch("/api/suggestions");
    const data = await res.json();

    suggestionList.innerHTML = "";

    data.suggestions.forEach((text) => {
      const btn = document.createElement("button");
      btn.className   = "sugg-btn";
      btn.textContent = text;

      btn.addEventListener("click", () => {
        closeSidebar();
        sendMessage(text);
      });

      suggestionList.appendChild(btn);
    });
  } catch (err) {
    console.warn("Could not load suggestions:", err);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
//  CORE CHAT LOGIC
// ═══════════════════════════════════════════════════════════════════════════════

function handleSend() {
  const text = userInput.value.trim();
  if (!text || isLoading) return;
  sendMessage(text);
}

async function sendMessage(text) {
  if (!text || isLoading) return;

  // Hide welcome screen on first message
  if (welcomeScreen && !welcomeScreen.classList.contains("hidden")) {
    welcomeScreen.classList.add("hidden");
  }

  // Clear the input
  userInput.value = "";
  autoResizeTextarea();
  updateSendBtn();

  // Append user bubble
  appendMessage("user", text);
  conversationHistory.push({ role: "user", content: text });

  // Show typing indicator
  showTyping();
  setLoading(true);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        history: conversationHistory.slice(-10), // send last 10 turns
      }),
    });

    const data = await response.json();

    hideTyping();

    if (!response.ok || data.status === "error") {
      appendMessage("bot", data.error || "Something went wrong. Please try again.", [], true);
    } else {
      appendMessage("bot", data.response, data.sources || []);
      conversationHistory.push({ role: "bot", content: data.response });
    }

  } catch (err) {
    hideTyping();
    console.error("Fetch error:", err);
    appendMessage(
      "bot",
      "⚠️ Cannot connect to the server. Make sure the Flask backend is running on port 5000.",
      [],
      true
    );
  } finally {
    setLoading(false);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
//  MESSAGE RENDERING
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Append a message bubble to the chat.
 * @param {string} role    - "user" or "bot"
 * @param {string} content - Raw text content
 * @param {Array}  sources - Source strings (bot only)
 * @param {boolean} isError - Show error styling
 */
function appendMessage(role, content, sources = [], isError = false) {
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = role === "user" ? "👤" : "🎓";

  const msgContent = document.createElement("div");
  msgContent.className = "msg-content";

  const bubble = document.createElement("div");
  bubble.className = `msg-bubble${isError ? " error" : ""}`;
  bubble.innerHTML = formatMessage(content);

  const meta = document.createElement("div");
  meta.className = "msg-meta";

  const timeEl = document.createElement("span");
  timeEl.className = "msg-time";
  timeEl.textContent = getCurrentTime();
  meta.appendChild(timeEl);

  // Add "Sources" button for bot messages with sources
  if (role === "bot" && sources.length > 0) {
    const srcBtn = document.createElement("button");
    srcBtn.className   = "source-btn";
    srcBtn.textContent = `📚 ${sources.length} source${sources.length > 1 ? "s" : ""}`;
    srcBtn.addEventListener("click", () => openModal(sources));
    meta.appendChild(srcBtn);
  }

  msgContent.appendChild(bubble);
  msgContent.appendChild(meta);

  row.appendChild(avatar);
  row.appendChild(msgContent);

  chatMessages.appendChild(row);
  scrollToBottom();
}

/**
 * Convert plain text with markdown-like syntax to HTML.
 * Handles: **bold**, *italic*, `code`, bullet lists, numbered lists, headers.
 */
function formatMessage(text) {
  if (!text) return "";

  // Escape HTML entities first
  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Headers: ### text
  html = html.replace(/^###\s+(.+)$/gm, "<h3>$1</h3>");

  // Bold: **text**
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // Italic: *text*
  html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");

  // Inline code: `code`
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");

  // Numbered lists: "1. item"
  html = html.replace(/^\d+\.\s+(.+)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>.*<\/li>)(\n<li>)/g, "$1$2"); // group them
  // Wrap consecutive <li> in <ol>
  html = html.replace(/((<li>[^]*?<\/li>\n?)+)/g, (match) => {
    // Check if first token looks like a number list (already converted)
    return `<ol>${match}</ol>`;
  });

  // Bullet lists: "- item" or "• item"
  html = html.replace(/^[-•]\s+(.+)$/gm, "<li>$1</li>");
  // Wrap consecutive <li> NOT already in <ol> in <ul>
  html = html.replace(/(?<!<\/ol>)((<li>[^]*?<\/li>\n?)+)(?!<\/ol>)/g, (match) => {
    if (match.includes("<ol>")) return match;
    return `<ul>${match}</ul>`;
  });

  // Paragraphs: double newline → <p>
  html = html
    .split(/\n\n+/)
    .map((para) => {
      para = para.trim();
      if (!para) return "";
      // Don't wrap block elements in <p>
      if (/^<(ul|ol|h[1-6]|li)/.test(para)) return para;
      return `<p>${para.replace(/\n/g, "<br/>")}</p>`;
    })
    .join("\n");

  return html;
}

// ═══════════════════════════════════════════════════════════════════════════════
//  TYPING INDICATOR
// ═══════════════════════════════════════════════════════════════════════════════

function showTyping() {
  typingRow = document.createElement("div");
  typingRow.className = "msg-row bot";
  typingRow.id = "typingIndicator";

  typingRow.innerHTML = `
    <div class="msg-avatar">🎓</div>
    <div class="msg-content">
      <div class="msg-bubble">
        <div class="typing-indicator">
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
        </div>
      </div>
    </div>
  `;

  chatMessages.appendChild(typingRow);
  scrollToBottom();
}

function hideTyping() {
  if (typingRow) {
    typingRow.remove();
    typingRow = null;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
//  SIDEBAR
// ═══════════════════════════════════════════════════════════════════════════════

function openSidebar() {
  sidebar.classList.add("open");
  sidebarOverlay.classList.add("open");
  document.body.style.overflow = "hidden";
}

function closeSidebar() {
  sidebar.classList.remove("open");
  sidebarOverlay.classList.remove("open");
  document.body.style.overflow = "";
}

// ═══════════════════════════════════════════════════════════════════════════════
//  SOURCE MODAL
// ═══════════════════════════════════════════════════════════════════════════════

function openModal(sources) {
  modalBody.innerHTML = "";

  if (!sources || sources.length === 0) {
    modalBody.innerHTML = `<p style="color:var(--text2);font-size:0.85rem">No sources available.</p>`;
  } else {
    sources.forEach((src) => {
      const item = document.createElement("div");
      item.className   = "source-item";
      item.textContent = src;
      modalBody.appendChild(item);
    });
  }

  modalOverlay.classList.add("open");
}

function closeModal() {
  modalOverlay.classList.remove("open");
}

// ═══════════════════════════════════════════════════════════════════════════════
//  CLEAR CHAT
// ═══════════════════════════════════════════════════════════════════════════════

function clearChat() {
  if (!confirm("Clear the entire conversation?")) return;

  chatMessages.innerHTML  = "";
  conversationHistory     = [];

  // Show welcome screen again
  if (welcomeScreen) {
    welcomeScreen.classList.remove("hidden");
  }

  // Reset active category button
  document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));

  closeSidebar();
}

// ═══════════════════════════════════════════════════════════════════════════════
//  HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

/** Auto-grow the textarea as the user types */
function autoResizeTextarea() {
  userInput.style.height = "auto";
  userInput.style.height = Math.min(userInput.scrollHeight, 140) + "px";
}

/** Enable/disable send button based on input content */
function updateSendBtn() {
  sendBtn.disabled = userInput.value.trim() === "" || isLoading;
}

/** Toggle loading state (disables input + send button) */
function setLoading(state) {
  isLoading         = state;
  sendBtn.disabled  = state;
  userInput.disabled = state;
  if (!state) {
    userInput.focus();
    updateSendBtn();
  }
}

/** Scroll chat to the latest message */
function scrollToBottom() {
  requestAnimationFrame(() => {
    chatContainer.scrollTo({
      top: chatContainer.scrollHeight,
      behavior: "smooth",
    });
  });
}

/** Return current time as HH:MM AM/PM */
function getCurrentTime() {
  return new Date().toLocaleTimeString("en-IN", {
    hour:   "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}
