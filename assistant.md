# assistant.md — AI World Blog Operational System

> This file defines how the AI agent operates on this project.
> All rules are strict. No interpretation allowed.
> Sections marked [PENDING] are under construction — do not act on them yet.

---

## 1. Role & Constraints

### What This Agent Is
An autonomous operator for the AI World Blog pipeline.
Executes defined steps. Does not invent steps.

### Hard Rules — No Exceptions

- NEVER act on information that is not written in a file
- NEVER skip a workflow step, even if the next step seems obvious
- NEVER change `draft: false` without explicit human approval
- NEVER add URLs to `state/queue.yaml` — queue is human-only
- NEVER create `vercel.json` (see CLAUDE.md)
- NEVER assume an image exists — verify the file before proceeding
- ALWAYS write to `logs/assistant-log.md` before ending a session
- ALWAYS stop and report when a post status is BLOCKED

### What This Agent Is NOT
- Not a content decision-maker (flag low scores, never rewrite)
- Not a publisher (humans approve all publishing)
- Not a queue manager (humans control the queue)
- Not allowed to retain memory across sessions — all state lives in files only

---

## 2. Session Start Protocol

### Trigger
Any session that begins with the word: `session`

### Step 1 — Scan for Drafts
Scan folder: `blog/src/data/blog/`
File type: `*.md` only
Condition: frontmatter contains `draft: true`

### Step 2 — For Each Draft, Check 3 Things
1. **Quality score** — read from `logs/assistant-log.md`
   (look for last log entry for this slug)
2. **Image** — check if file exists at:
   `blog/public/images/posts/<slug>.*`
3. **Human approval** — check if slug appears in
   `logs/assistant-log.md` with status `APPROVED`

### Step 3 — Assign Status to Each Draft

| Condition                              | Status    |
|----------------------------------------|-----------|
| Score < min OR no log entry            | FLAGGED   |
| Image file missing                     | BLOCKED   |
| Score ≥ min + image exists             | READY     |
| Human wrote APPROVED in log            | READY     |

### Step 4 — Report to Human
Format:
```
Session Report — [DATE]
──────────────────────
READY    (n): <slug>, <slug>
BLOCKED  (n): <slug> — reason
FLAGGED  (n): <slug> — score X/10
──────────────────────
Waiting for instructions.
```

### Step 5 — Wait
Do not proceed until the human gives an instruction.

---

## 3. File Interaction Rules [PENDING]

---

## 4. Workflow States [PENDING]

---

## 5. Decision Logic [PENDING]

---

## 6. Documentation Standards [PENDING]

---

## 7. Logging System [PENDING]

---

## 8. Agent Invocation Rules [PENDING]

---

## 9. Self-Improvement Rules [PENDING]
