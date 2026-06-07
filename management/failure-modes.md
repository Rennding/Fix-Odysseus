# Failure Modes

Living table. Add a row when (1) a new pattern repeats, (2) a rule fails, or (3) Claude invents a workflow on the fly. Filter: changes future behavior + generalizes + not already in `CLAUDE.md`.

To look up a pattern: `grep -in '<keyword>' management/failure-modes.md`

To add a row: append to the table below. Do not use the em-dash glyph in new rows (see the em-dash row); use a comma, semicolon, colon, period, or parentheses instead.

These seed rows are stack-agnostic and process-level, so they apply to any project under this pipeline. Project-specific failure modes (a library quirk, a domain invariant) get appended as they surface.

| Failure | Avoidance |
|---|---|
| Spec drift | Ambiguous spec instruction: stop and ask, never guess. |
| Fixing unrelated bugs mid-session | Note in the report, do not fix. Scope creep corrupts sessions. |
| Queue item bypasses GitHub | Open an issue first. GitHub is the source of truth. |
| GitHub and local state desync | Sync GitHub issues at session start before touching anything. |
| Build marked done without QA gate | Build sessions: mark `needs-review` plus post a QA Brief. Never `qa-pass` until Aram approves. |
| QA Brief written as a dev changelog | Write for someone with no memory of the issue: what they will see, where to look, what broken looks like. |
| Plan plus Build in one session | Never. Every item is exactly one type. Split into separate issues. |
| DEVLOG drifts from GitHub | After any GitHub issue update, mirror to `DEVLOG.md` in the same operation. GitHub first, local second. |
| Edit without an anchor grep | Before every edit: grep the exact target string, confirm it matches exactly once, then edit. |
| GitHub MCP unavailable in session | Work local-only immediately. Note every needed GitHub write in the session report for Aram. |
| Orphan branch (no issue, no PR) | Every branch ties to an open issue through `[#NN]` commits and the PR `Closes #NN` line, not through the branch name. Never delete a branch without Aram's OK. |
| Commit without an issue ref | `[#NN] subject` prefix. `[#infra]` for meta work. Reject vague messages like "edits" before staging. |
| PR opened without `Closes #NN` | The PR body must include `Closes #NN` (or `Refs #NN` for partial). Double-check the body before submitting. |
| `qa-improve` / `qa-fail` applied via label only | Async verdicts are supported (CLAUDE.md §9). The `spec-ready` gate is still required before a build starts; the follow-up SPEC is drafted first. |
| Reading whole files for orientation | Grep for the exact symbol; use the §14 generator once it exists. Never open a whole module to find a function. |
| CLAUDE.md duplicates on-disk reference content | Reference by path. Never copy `PROJECT.md` or `management/templates/*` into CLAUDE.md or a SPEC body. On drift, the on-disk file wins (§0.1). |
| Building before §4 is filled in | Halt. The stack-decision is a hard prerequisite for any Build or Improve session (§0.1). |
| Push to `main` or force-push | `main` is PR-only, squash-merge. No exceptions. Force-push is forbidden on every branch, always. |
| Session assumes stale state from a prior run | Sessions are stateless; GitHub is the memory. Re-list open issues at session start; never act on a remembered queue. |
| Stream idle timeout on long writes | For large markdown or config files (about 250-plus lines), write a skeleton first, then `Edit`-append section by section. Each call streams a moderate output and avoids the idle-timeout window. |
| Dead-gap "No response requested" non-response | Never emit "No response requested." as a full turn. If the last user message has a question, an imperative verb, or an invitation to ask, the turn must include a tool call or a substantive reply. If unsure whether action is wanted, ask one clarifying line; never go silent. |
| Follow-up commit pushed to an already-merged branch | The moment a PR merges, the old branch is dead. New or pending changes go on a new branch plus new issue plus new PR. A commit on a merged branch is invisible to Aram and cannot be squash-merged. |
| Auto-opening a PR on a branch not freshly off `main` | Before any PR action, verify `git log --oneline origin/main..HEAD` and the open-PR list. A long-lived working branch can carry far more than one session's scope; auto-opening a PR there mis-scopes `Closes #NN`. In that state, push the session's files and surface the branch state to Aram for the call. |
| Option-listing before disambiguating compound wording | When a user statement has two coherent reads that imply different shapes, ask the disambiguation before listing options. Skipping it risks recommending the wrong shape entirely. |
| Compound Plan decisions split when they are coupled | Two decisions are one when picking them apart risks an incoherent answer (stack and content pipeline, schema and ingestion). Plan them together; §8 grouping still applies at the SPEC and build level. |
| Build replicates markup from a design reference | Design references (HTML mocks, Figma exports, screenshots) supply visual tokens: color, type, spacing, layout intent. Not implementation. Stack-native components are stack-shaped, not reference-shaped. Extract intent, not markup. |
| Tool or model picked without surveying the field | At Plan time for any tool, library, or model choice, enumerate every candidate in the same vendor or runtime family plus one or two adjacent families. One line each: capability, runtime, cost or license. The chosen tool is the survivor of an explicit comparison, not the first one named. |
| Plan reshapes an open downstream issue without updating its body | When a Plan moves work out of an existing open build issue, update that issue's body in the same commit that updates the parent SPEC. Source-of-truth (SPEC) and queue (issue body) drift otherwise. |
| Issue body cross-references a sibling created in the same batch | Issue numbers are assigned at creation, so a body written before the call cannot know a sibling's number. Create sequentially with the known parent number, or create the batch then immediately update the cross-ref. |
| Behavioral acceptance the build cannot exercise | When the spec lists a behavioral acceptance (tap, see, open the app) but the build adds no surface to exercise it (pure data layer, types, infra), land what you can verify (the gate, code review) and state in the QA Brief that the behavioral check is deferred to the first consuming feature. Do not fabricate steps; do not silently drop the criterion. |
| Acceptance needs real-device or platform verification | When an acceptance hinges on platform behavior the container cannot run (camera, push, OS TTS, installed-PWA behavior), enforce the safety-relevant invariant in code so it holds everywhere, verify the API contract against docs, and record device confirmation as the human-QA step. Do not claim you tested it. |
| Scaffold tool subcommand vanished between SPEC and Build | When a SPEC names a CLI subcommand, verify it still exists in the version actually installed before wiring scripts; upstream tools delete subcommands across majors. On absence, substitute the canonical replacement and update the SPEC plus CLAUDE.md §4 in the same session. |
| Fresh remote container has no installed dependencies | A web session clones the repo without dependencies, so the validation gate reds with phantom missing-module errors across files you never touched. Run the install (npm ci, or the stack equivalent) before trusting the gate. A wall of missing-module errors means deps are absent, not that you broke something. || Synthesis over verification | Assertions and multi-step recommendations drawn from training rather than immediate context are high-risk. Categories per §0.1 (a through h). Tells: anchoring on the user's framing instead of restating the goal in your own words; bias toward sophisticated paths when a boring native feature solves it; premature concreteness (token scopes, file paths, UI labels, version pins) before the path is verified. Correct shape: open with the §6 "Path before detail" line (Goal, Path, Source); wait for acceptance; if Source is training or unsure, verify before writing detail. Failure to grep this row when responding in any category is itself the bug. |
| Em-dash in Claude-authored output | The em-dash glyph reads as an LLM tell. Do not use it in any text Claude authors going forward: SPECs, issue and PR bodies, commit messages, code comments, chat, and new rows in this file. Replacements by context: comma, semicolon, colon, period, line break, parentheses, " · ". The shipped operating files (CLAUDE.md, README, HOW_TO_USE, the templates) predate this rule and keep their punctuation; the rule applies forward to new content, not as a retroactive sweep (do not fix unrelated files mid-session). Each phase that authors markup greps the changed files for the glyph before closing. |
