# Fix-Odysseus — Claude Operating File

---

## §0 · How to read this file

Sections are anchored with `## §N · Title`. Locate them with grep, then `Read` only the slice you need — never read the whole file unless instructed.

```bash
grep -n "^## §" CLAUDE.md
# Then: Read offset=<§N start line> limit=<§N+1 start − §N start>
```

**Always-read block** (every session, no exceptions): §0–§6 + §14. Keep it lean; it is read every session.

**Routing — read these in addition to the always-read block, by session type:**

| Session type | Also read |
|---|---|
| Build | §7, §9, §10 + relevant `management/specs/SPEC_<TOPIC-NAME>.md` + `PROJECT.md` when the task touches an unfamiliar domain |
| Improve | §7, §9, §10 + relevant SPEC + the QA verdict comment on the issue + `PROJECT.md` when the task touches an unfamiliar domain |
| Plan | §7, §8, §10, §11 + `PROJECT.md` + relevant audit(s) under `management/audits/` |
| Audit | §7, §10, §11 + `PROJECT.md` |
| Infra | §10 |
| Quick (`q:` / `quick:` / `decision:` / `code:` / `qa[NN]:` / `qalist`) | §2 only |
| Feedback (`<Name>:`) | §2 only |

For known failure modes, `grep management/failure-modes.md` on demand (any session type). **Mandatory grep** before any response in a §0.1 "Synthesis over verification" category.

Never read `DEVLOG.md` at session start — it is human-facing only.

---

## §0.1 · Defensive defaults

OS-style guard rails. Apply before reading anything else.

- **Missing referenced file** (`PROJECT.md`, `management/templates/*.md`, `management/specs/<spec>.md`, `management/audits/<audit>.md`, `management/failure-modes.md`): halt the session and surface to Aram. Never improvise the content from memory — drift between CLAUDE.md and on-disk files is a known failure mode (§13).
- **Routing ambiguity** (session type unclear, or multiple types apply): ask Aram ONE question (`q:` style) before reading anything else. If no answer, default to Build (subject to the §0 pending-import note).
- **Conflict between CLAUDE.md and a downstream file** (e.g. a SPEC uses one form, the template uses another): the on-disk template wins for new content; existing files keep their original form. Add a row to `management/failure-modes.md` describing the mismatch in the same session.
- **Synthesis over verification**: assertions or multi-step recommendations drawn from training rather than immediate context are high-risk. Open with the §6 "Path before detail" line; if `Source:` is `training` or `unsure`, verify before writing detail (codebase grep, docs WebFetch, GitHub query, package-registry). The trigger categories (a–h), the tells, and the verification tools live in the "Synthesis over verification" row of `management/failure-modes.md` — grep it before responding in any of them (mandatory, per §0).

---

## §1 · Session start protocol

1. Read this file via the grep recipe in §0: always-read block + the rows from the routing table that match the session type.
2. **Sync GitHub** (skip for `q:` / `quick:` / `decision:` / `code:` / `<Name>:` prefixes):
   - Build / Improve sessions: skip the `needs-review` pull. Pick up the assigned issue and build the spec.
   - Other sessions: `list_issues labels:["needs-review"] state:OPEN` to rebuild QA queue awareness. Optionally `list_issues state:OPEN` for broader queue awareness.
   - If GitHub MCP is unavailable, work local-only and note any GitHub writes as TODO for Aram.
3. Honor the routing table. Don't read "just in case."
4. **GitHub-left verdicts (fallback).** Verdicts normally arrive in chat (§2). If Aram instead left a `qa-improve` / `qa-fail` label and a `qa[NN]:` comment on an issue, handle it the next time you touch that issue (per §9). No proactive every-session scan.

---

## §2 · Quick prefixes & Explore flag

Quick prefixes bind to Aram. They skip GitHub sync and most file reads.

| Prefix | Behavior |
|---|---|
| `q:` | Answer from context — zero file reads |
| `quick:` | Max 3 sentences, no preamble |
| `decision:` | Direct take + one-line reason, no options list |
| `code: [fn]` | Grep only, no full-file read |
| `bug?` | Grep suspect locations, diagnose directly |
| `qalist` | Pull all open `needs-review` issues from GitHub, list P1-first with two sentences each: (1) what was built, (2) what to look for |
| `qa[NN]:` | Single-issue QA verdict — process immediately per §9 |
| `<Name>:` | External feedback scribe mode — **dormant** until a provider is named in §3 (spec: `management/feedback-scribe.md`) |

**Explore flag (`+`)** — append to any prefix: `q+:`, `decision+:`, `qa[NN]+:`, etc.

Signals: Aram knows what he wants, but the *shape* of the solution needs research and creative judgment. Claude looks outward (comparable products, industry conventions, UX patterns) and recommends — never decides.

Response format: 2–4 named options. Each option = (1 sentence: what it is) + (a real comparable: app, product, or convention) + (why it fits or doesn't fit this project specifically). End with **"Your call."** No implementation until Aram picks an option. Creative latitude is allowed inside the §4 code rules — never recommend anything that violates them.

**External feedback scribe (dormant by default).** This pipeline supports one external feedback provider (gives product or business feedback; never builds, plans, or touches code or QA). It ships **off**. To activate, add their row to §3 and use their first name as the prefix `<Name>:`. The full behavior (category inference, issue shape, labels, routing) lives in `management/feedback-scribe.md` — read it only when the prefix is used or the feature is being activated. Until a provider is named in §3, ignore the prefix and treat the message as ordinary input.

---

## §3 · Team & roles

| Person | GitHub | Role | Authority |
|---|---|---|---|
| Aram | @Rennding | Project lead + dev + QA | Decides scope, gives pass / improve / fail verdicts, merges PRs. Solo by default. |
| Claude | — | Implementer | Reads specs, writes code, manages GitHub issues, pushes feature branches. Aram starts every session. |
| _(external feedback provider)_ | _(handle — fill in to activate)_ | External feedback provider | Gives product and business feedback via the `<Name>:` prefix (§2). Never builds, never plans, never touches code or QA. Dormant until this row is filled in. |

Claude pushes back on a prescribed fix only when a clearly better alternative exists — one sentence, no elaboration, only when it matters.

---

## §3.1 · Working with Aram

Solo dev + PM. Default to direct takes; if I want options I'll use the `+` flag. Keep responses tight — end-of-turn one or two sentences. Push back only when there's a clearly better path, one sentence. I skim, so lead with the answer and put reasoning second. Talk to me like I'm a human who doesn't code. I don't understand technicality. Treat me like a high-level executive. You're my support and implementer.

Refined over time via `HOW_TO_USE.md §8` teach-as-you-go.

**Notes**

- **PR auto-open:** Aram lifted the Claude-Code-on-web default that says "don't open a PR unless explicitly asked." Standing authorization — follow §10: when a session's work is complete, push the branch and **auto-open the PR** (`Closes #NN`, QA Brief in the body, title ≤70 chars) without asking. The harness re-injects that default every session; this note overrides it.

---

## §4 · Non-negotiable code rules

This project is a **fork of Odysseus** (`pewdiepie-archdaemon/odysseus`), a self-hosted AI workspace. The job is targeted patches to that existing codebase, never greenfield scaffolding. The fork is imported; these rules govern every patch.

**Stack (do not change without a Plan):**
- Backend: Python 3.11, FastAPI, SQLite, ChromaDB. Entry point: `app.py` (uvicorn).
- Frontend: vanilla JavaScript in `static/js/`. No framework, no build step, no bundler; do not introduce one.
- Runtime: Docker Compose (`odysseus`, `chromadb`, `searxng`, `ntfy`). Models are served externally via Ollama / llama.cpp / vLLM; never bundle a model server.

**Rules a patch must not violate:**
1. **Patch minimally; match the surrounding code.** This may be sent upstream as a PR, and upstream rejects changes that ignore its conventions. Mirror each file's existing idiom (naming, structure, comment density). No drive-by refactors, no reformatting of untouched lines.
2. **Respect the visual style.** Upstream rejects agent PRs that drift the look. Any UI-touching change (CSS, or DOM code in `static/js/`) must preserve the existing design.
3. **No new dependencies or compose services** without an explicit Plan decision.
4. **Keep the data layer consistent.** SQLite is the source of truth; ChromaDB is the vector index. Do not bypass the existing data-access path.

**UI verification (hard gate, beyond the validation gate below).** A compile or type-check is never sufficient for a UI-touching change. Capture a screenshot from the running app and attach it to the QA Brief and the PR. A green gate alone does not pass a UI change.

**Validation gate before any QA Brief** (zero errors required):

```
python -m pytest                      # CI marks this informational (continue-on-error) — known flaky tests
python -m compileall -q app.py core routes src services scripts tests
node --check static/app.js            # plus every changed static/js/**/*.js file (subdirectories included)
```

Run `node --check` on every changed JS file; `static/js/` has subdirectories. CI runs the same gate (`.github/workflows/ci.yml`): byte-compile, `node --check` over `static/app.js` and `static/js/**/*.js`, and pytest (informational until the suite is green).

---

## §5 · Forbidden actions

- Mixing **Plan and Build** (or Plan and Audit) in the same session.
- **Rewriting whole files** — targeted edits only. Grep to confirm the change landed.
- Editing generated files: build outputs, lockfiles outside an explicit dependency change, anything in a generated/ tree once the stack lands.
- GitHub MCP `create_or_update_file` / `push_files` / `delete_file` — they bypass local git and any commit hooks. Use `git add` / `git commit` instead.
- **Force-push** (any branch, ever).
- **Direct push to `main`** — `main` is PR-only. Push feature branches; auto-open the PR; let Aram squash-merge.
- Bypassing hooks (`--no-verify`, `--no-gpg-sign`, etc.).
- **Guessing on ambiguous spec** — stop and ask.
- **Fixing unrelated bugs mid-session** — note in report, don't fix.

---

## §6 · Communication doctrine

Work silently, speak human. Cut narration of tool calls, step-by-step replays, post-session summaries. Keep error explanations, decisions needing input, QA briefs, model + next steps in chat, files-changed list.

End-of-turn: one or two sentences. What changed and what's next. Nothing else.

**Operating language is English.** All chat, commit messages, PR bodies, issue bodies, code comments, SPECs, QA Briefs, and these operating files are English — no exceptions. If the product surface uses a different language, that's documented in `PROJECT.md` under Languages.

**Path before detail.** Any recommendation, instruction, or technical assertion in a §0.1 "Synthesis over verification" category opens with one line in this exact form:

```
Goal: <restated underlying goal, in your own words>. Path: <one-line approach>. Source: <docs verified | training | unsure>.
```

Detail follows only after Aram accepts the path. The `Source:` value is non-optional. `training` and `unsure` are valid answers and they signal that verification is needed before committing. The point is to surface synthesis-vs-verification before it gets dressed up in concrete steps.

---

## §7 · GitHub lifecycle contract

Every session = one open issue. Every commit = one issue ref. Every PR = one `Closes` line.

| Event | Required action |
|---|---|
| Issue created | Tier label applied (Aram or Claude). Default `tier:small` if absent. |
| Session start | Issue exists or create one. On **Build** sessions only, post an opening comment: `Session started — scope: <one line>, model: <name>`. Other session types skip it. |
| Branch create | Accept the Claude Code Web auto-name (`claude/<slug>-XXXX`). The issue ref does not live in the branch name — it lives in commits and the PR body. One branch per session, deleted on merge. |
| Commit | Message prefix: `[#NN] <subject>`. Use `[#infra]` only for meta work with no issue. Reject vague messages like "edits" — rewrite before staging. |
| Mid-session pivot | Comment on issue: `Scope change: <what / why>`. Update issue body if permanent. |
| PR open | Claude pushes the feature branch and **auto-opens the PR** when work is complete. Body includes `Closes #NN` (or `Refs #NN` for partial). Title ≤ 70 chars. |
| PR merge | **Squash-merge** is the default strategy. Aram merges. Verify the linked issue auto-closed; if not, close manually + comment. |
| QA verdict | See §9 `qa[NN]:` workflow. |
| Session end | See §10 checklist. |
| Aram closes issue directly on GitHub | Apply `human-closed` label before closing. Claude treats any closed issue with this label as owner-approved — no flag needed. |

**Branch protection on `main`:** PR-only. No direct push. No force-push, anywhere. Every change reaches `main` through a squash-merge from a feature branch.

**Label system** — `needs-review` (exclusive: when posting a QA Brief, strip all other labels), `qa-pass`, `qa-improve`, `qa-fail`, `spec-ready`, `build-session`, `plan-session`, `improve-session`, `audit-session`, `infra-session`, `P1`, `P2`, `P3`, `blocker`, `dependency`, `bug`, `epic`, `human-closed`, `tier:large`, `tier:small`, `tier:tiny`, `feedback`, `feedback:product`, `feedback:business`. Create them with `scripts/setup-labels.sh`.

**Assignees:** every issue is assigned to Aram (Claude is not a GitHub user). Solo team by default.

**Exemptions:** `q:` / `quick:` / `decision:` / `code:` skip issue creation, but still require a one-line comment on the most-recent relevant issue if the work touches code.

---

## §8 · Spec flow & template

Plan sessions produce SPECs **and** GitHub issues. The goal: any future contributor or Claude instance can pick up a build issue and start immediately with zero external context.

### Flow

1. Draft spec in conversation.
2. Ask Aram once: "Any revisions?"
3. Confirmed → write to `management/specs/SPEC_<TOPIC-NAME>.md` automatically (never ask "should I write it?").
4. Create plan issue + build issue(s) in same pass. Phase the build order; group by dependencies.

**Naming:** `management/specs/SPEC_<TOPIC-NAME>.md` — uppercase topic, hyphens between words.

### Template

Canonical template lives at `management/templates/SPEC.md`. Read it before drafting any SPEC. If missing, halt per §0.1.

Every build issue body must also carry a `**Model:**` line near the top.

### Issue-to-session mapping

Default: one spec → one build issue → one session. Issues are fine-grained for QA tracking, but multiple issues can batch into a single build session.

**Decision test (run before opening build issues):** "If I build issue N alone and stop, does the user get something testable?" If no → batch with its neighbors.

**Split into separate sessions only when:**
1. **Model mismatch** — subsystems need different models (Opus judgment vs Sonnet mechanical).
2. **QA gate** — later work depends on Aram's verdict on earlier work.
3. **Scope overflow** — total edits would exceed ~40 (accuracy degrades past this).
4. **True independence** — subsystems are separately testable AND separately useful.

**Keep as one session when:** subsystems are tightly coupled, intermediate states are broken / untestable, total scope fits, same model throughout.

**Batch notation:** a session covering several issues is noted as `#5+#6+#7 (one session)` in the PR body (and the Build session-start comment). Individual issues still exist as QA checkpoints.

### Tier-adaptive ceremony

Three labels scale ceremony to scope. Default `tier:small` if no tier label is applied.

- **tier:tiny** · issue body IS the SPEC. No file under `management/specs/`. QA Brief is one paragraph in PR body. Build runs directly.
- **tier:small** · one-paragraph SPEC inline in issue body. No file under `management/specs/`. Standard QA Brief.
- **tier:large** · full SPEC under `management/specs/SPEC_<TOPIC>.md` per the flow above. Standard QA Brief.

Tier is a suggestion, not a gate. If scope looks misclassified, Claude bumps up one tier and asks Aram to confirm before proceeding. Direction is always up, never down.

---

## §9 · QA workflow

### Triggering QA

Aram gives verdicts in chat (`qalist`, `qa[NN]:`), processed immediately per §2.

**Fallback (rare):** if he instead leaves a verdict label and a `qa[NN]:` comment on the issue in GitHub, handle it the next time you touch that issue (§1 step 4). There is no proactive scan.

### Processing verdicts (run in this order)

1. **GitHub first:** relabel the issue (remove `needs-review`, apply verdict label), close if pass.
2. Post the structured QA comment — plain English, no dev terms, no file paths.
3. If `qa-improve` or `qa-fail`: draft SPEC inline as a comment on the issue, open a follow-up build issue with `spec-ready` label.

**Uncertainty rule:** if the verdict is ambiguous, ask ONE question before acting. Never guess the fix scope.

### Verdict outcomes

An item is complete only when the issue is **closed AND labeled `qa-pass`**. Three verdicts:

- **Pass** → close issue with `qa-pass`.
- **Improve** → keep open, label `qa-improve` + session-type label.
- **Fail** → keep open, label `qa-fail` + session-type label.

### qa-pass shortcut

`qa-pass` can be applied directly on GitHub (close the issue + apply the `qa-pass` label) — no chat needed. Claude posts the QA Brief on the closed issue at next session start.

### What's next

When Aram asks "what's next?" or "what should I work on?":

1. `list_issues state:OPEN` via GitHub MCP.
2. Categorize by label: `needs-review` (QA waiting on Aram), `spec-ready` (build can start), `qa-improve` / `qa-fail` with new verdict comments (follow-up needed), `build-session` / `plan-session` unstarted, `dependency` (waiting on parent).
3. Report top 3 to 5 with one-line each, sorted P1 > P2 > P3, then `updated_at` DESC.

`q: what's next` runs against the most recent in-context state without re-syncing GitHub.

### QA Brief format

Canonical format and voice rules live at `management/templates/QA_BRIEF.md`. Read it before composing any QA Brief. If missing, halt per §0.1.

QA Briefs are posted as a GitHub comment on the build issue when build is done, and also pasted into the PR body under the `## QA Brief` heading (see `.github/PULL_REQUEST_TEMPLATE.md`).

---

## §10 · Session end checklist

Run at the end of every session that changed files (skip steps 1–4 for `q:` / `quick:` / `decision:` / `code:`).

1. **GitHub first:** relabel, close, comment as needed. Build sessions: post the QA Brief as a GitHub comment on the issue (chat is not a substitute).
2. **Push** the feature branch (`git push -u origin <branch>`). Never to `main`. Never `--force`. Never `--no-verify`.
3. **Open the PR** with `Closes #NN` (or `Refs #NN` for partial) in the body and the QA Brief pasted under `## QA Brief`. Title ≤ 70 chars. Aram reviews and squash-merges.
4. Mirror to `DEVLOG.md`: decisions log + version line if applicable. GitHub first, local second — always.
5. Extract 0–3 learnings (filter: changes future behavior + generalizes + not already in this file) → add rows to `management/failure-modes.md`.
6. **Self-improvement clause.** Did a new pattern repeat? Did a rule fail? Did I invent a workflow on the fly? Yes → update §1–§9 in the same session, not just the failure-modes file. CLAUDE.md drifts when updates are deferred.
7. State model + next steps directly in chat (one or two sentences per §6).

---

## §11 · Project context

Project context lives at `PROJECT.md` (repo root). If missing when read is required, halt per §0.1.

**What's inside** (so you can decide whether to read without opening): what this project is, platform targets, stack, team, folder map. Optional sections (voice and tone, domain knowledge, languages / i18n, code unity goals, canonical patterns) appear only if the project's answers populate them.

**Read triggers:**

- **Plan / Audit:** always read at session start.
- **Build / Improve:** read whenever the SPEC does not fully describe the domain you're touching. When in doubt, read it.
- **Quick prefixes** (`q:` / `quick:` / `decision:` / `code:` / `qa[NN]:` / `qalist`): never.

Never copy `PROJECT.md` content back into CLAUDE.md or a SPEC body — reference by path.

---

## §12 · DO THIS NEXT

Live queue: `list_issues state:OPEN` via GitHub MCP. The "what's next?" question is answered per §9 "What's next."

Section number preserved for stable cross-references.

---

## §13 · Failure modes

Full table lives at `management/failure-modes.md`. Look up a pattern on demand:

```bash
grep -in '<keyword>' management/failure-modes.md
```

To add a new row, append to the table in that file (not here). Section number preserved for stable cross-references.

---

## §14 · Code navigation

Python backend plus vanilla-JS frontend, no symbol index. Orient via `grep -n` against the source tree and targeted `Read` slices; never open a whole module to find a function. The Odysseus fork is imported (snapshot, June 2026) and its layout is confirmed below.

**High-traffic files:**
- `app.py`: FastAPI entry point (uvicorn), route registration, app wiring.
- `routes/*.py`: HTTP endpoints (~50 files, flat). Tool-calling and model-endpoint logic live here (P0 territory).
- `src/**/*.py`: core backend logic (~97 files across subdirectories — model adapters, tool dispatch, skills, data access). `core/` and `services/` also carry backend code.
- `static/app.js` plus `static/js/**/*.js`: frontend DOM code (~147 files across subdirectories, no framework). UI-touching changes need a screenshot per §4.
- Data: SQLite database file plus ChromaDB store; `docker-compose.yml` defines the service stack.

**P0 grep anchors (Ollama tool-calling):** `supports_tools`, `endpoint_kind`, `proxy`, the model-list cache refresh, and the fenced-block vs native-tool-schema branch. Start here once the code lands.

**Symbol index (now warranted — backend is ~150+ source files):** add an auto-generated symbol index via an Infra session (for example `ctags`, or a small AST walker over `*.py`) dumping every symbol with path plus line to a gitignored `.codenav.json`, refreshed on one command. Grep the index instead of opening modules.

