# Attended Pipeline Template

Drop this kit into a fresh repo, confirm a few inferred defaults on the first session, and you have a working, fully-attended Claude operating model: one issue per session, one branch, one PR, a QA gate you control, and a `CLAUDE.md` that teaches itself over time.

This is the **attended** sibling of the unattended idea-to-product pipeline. No routine, no orchestrator, no laptop-closed automation. **You drive every session by chatting** — Claude infers the session type, opens the GitHub issue, writes the code, runs the gate, posts a QA Brief, and opens the PR. You review and squash-merge.

It is **project-agnostic** (no product baked in) but **personalised to Aram** — the working style, the speed prefixes, and the team are already set. Drop it into any new repo and go.

## What you do (once per repo)

1. Copy the **contents** of this folder to the **root** of a fresh repo, so `CLAUDE.md`, `PROJECT.md`, `HOW_TO_USE.md`, `DEVLOG.md`, `AGENTS.md`, and the `management/`, `scripts/`, `.github/`, and `.claude/` folders all sit at the top level. Push to GitHub.
2. Create the GitHub labels: run `bash scripts/setup-labels.sh` (needs the `gh` CLI), or create them by hand from the list in that file.
3. Connect the repo to Claude Code and start a session. Say anything — the first session proposes sensible defaults for you to confirm in one round, writes your project files, and erases its own bootstrap block in one commit.
4. From then on, just chat. See `HOW_TO_USE.md`.

## What's in this kit

| Path | What it is |
|---|---|
| `CLAUDE.md` | The operating model Claude reads every session: session protocol, code rules, GitHub lifecycle, spec flow, QA workflow. Carries the slim first-run bootstrap (§0.0) that self-erases. |
| `PROJECT.md` | A `<<NEW_PROJECT>>` marker stub. The first session replaces it with real project context. |
| `HOW_TO_USE.md` | Aram-facing tutorial: how to drive sessions, the speed prefixes, the QA loop, teach-as-you-go. |
| `DEVLOG.md` | Human-facing decisions log, mirrored from GitHub. Never read by Claude at session start. |
| `AGENTS.md` | Tombstone pointer to `CLAUDE.md` for tools that look for `AGENTS.md`. |
| `management/templates/` | Canonical `SPEC.md` and `QA_BRIEF.md` templates. |
| `management/failure-modes.md` | Stack-agnostic failure-mode table, seeded; grows as you go. |
| `management/feedback-scribe.md` | Spec for the dormant external-feedback prefix (off until you name a provider in §3). |
| `management/specs/` · `management/audits/` | Where SPECs and audit reports land (empty at first). |
| `scripts/setup-labels.sh` | Creates the GitHub label set the pipeline runs on. |
| `.github/ISSUE_TEMPLATE/` · `.github/PULL_REQUEST_TEMPLATE.md` | Five session issue templates and the PR template (with the `## QA Brief` slot). |
| `.github/workflows/ci.yml` | Guarded CI: passes on an empty repo, runs the npm validation gate once an app exists, and fails on an em-dash in changed SPECs / audits / source. Adjust for a non-npm stack. |
| `.claude/` | Optional Claude Code automation: a SessionStart hook (installs deps + nudges the operating file), a read-only permission allowlist (fewer prompts), and slash commands (`/whatsnext`, `/qa`, `/plan`, `/audit`) that wrap the prefix flows. |

## Attended vs unattended

- **Attended (this kit):** you are in the loop every session. You start it, steer it, give the QA verdict, and merge. Best when you want judgment on each step.
- **Unattended (the other kit):** a scheduled routine fans out into several PRs while you sleep; you wake up and review. Best for breadth without typing prompts.

Same operating model underneath (`CLAUDE.md` §7-§10). The difference is who pulls the trigger.

## Notes

- **Stack is your choice at first run.** Pick one when Claude proposes defaults and it fills in `CLAUDE.md` §4; or say "TBD" and the first real session is a stack-decision Plan. Build and Improve sessions are blocked until the stack lands.
- **External feedback provider** (the `Cihan:`-style scribe) ships **dormant**. Name a provider in `CLAUDE.md` §3 to activate the feedback prefix; until then it is off.
- After the first session runs, this README is replaced by a one-screen overview of your actual project.
