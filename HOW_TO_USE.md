# How to use Claude on Fix-Odysseus

A short, conversational tutorial. The pipeline is small once you see the shape of it.

---

## §1 · The 30-second version

You don't learn the pipeline. **Claude reads `CLAUDE.md` at the start of every session — that's the pipeline.** You just chat.

Open Claude Code, describe what you want in plain English, and Claude figures out the rest: which session type this is, what to read, which GitHub issue to open, which branch to use, which commit message to use, when to ask you a question, when to stop and post a QA Brief.

Your job: describe what you want, answer when Claude asks, review the PR Claude opens.

> **Today's caveat:** if the stack hasn't been picked yet, Build / Improve sessions are blocked until that decision lands (`CLAUDE.md` §0.1). Plan, Audit, and Infra sessions all work today.

---

## §2 · Your first session

Open Claude Code in this repo. The very first session runs a short first-run setup: Claude proposes sensible defaults (project name, platform, repo, stack) for you to correct in one round, asks only for the one-line description, shows you exactly what it will write, and on your "go" sets up your project files in one commit. After that, you're operating.

From then on, type what you want, like you would to a co-worker who already knows the codebase. Examples that work:

> "Plan the main flow — what does a user see when they open the app cold."

> "Audit the repo for anything still leaking from the template."

> "The empty-state copy feels off. Improve it."

> "Add a prepush hook that runs the validation gate."

That's it. Claude will:

1. Pick the session type (Build / Plan / Improve / Audit / Infra).
2. Read only the parts of `CLAUDE.md` that matter for that type.
3. Open or pick up a GitHub issue, post a "session started" comment.
4. Ask you a question if the spec is ambiguous — answer in one line.
5. Edit code, commit with the right `[#NN] subject` prefix, push the feature branch, and **auto-open the PR** with `Closes #NN` in the body.
6. Tell you what changed and what to do next.

You review the PR and squash-merge when CI is green.

---

## §3 · The five session flavors

You don't have to name the flavor — Claude infers it from what you say. But it helps to know what each one does.

| Flavor | When to use it | What you say |
|---|---|---|
| **Build** | You have a spec (or a clear ask) and want code written. *Blocked until the stack is picked.* | *"Build issue #42."* / *"Add a saved-items tab."* |
| **Plan** | You want to think through a feature before writing code. Claude produces a SPEC and opens build issues. | *"Plan how a user saves something for later."* |
| **Improve** | Something exists but QA (or you) said it's not right. *Blocked until the stack is picked.* | *"Improve the main view — QA on #51 came back qa-improve."* |
| **Audit** | You want a read on a subsystem. No code changes, just findings. | *"Audit the data layer for divergent patterns."* |
| **Infra** | Repo plumbing, CI, scripts, configs — meta work without a feature issue. | *"Add a prepush hook that runs the validation gate."* |

**Rule that matters:** never mix flavors in one session (`CLAUDE.md` §5). If you ask Claude to "plan and build" something, Claude plans first, asks you to confirm, then starts a fresh build session. That's intentional — accuracy collapses when flavors mix.

---

## §4 · Speed prefixes

The biggest day-to-day win. Stick a prefix on the front of your message and Claude **skips GitHub sync, skips most file reads, and answers fast.**

| Prefix | What you get | Example |
|---|---|---|
| `q:` | Answer from context. Zero file reads. | `q: where does the team table live?` |
| `quick:` | Max 3 sentences, no preamble. | `quick: why are Build sessions blocked right now?` |
| `decision:` | A direct take + one-line reason. No options list. | `decision: should items be tags or first-class entities?` |
| `code: [fn]` | Grep-only. Doesn't open the whole file. | `code: handleSubmit` |
| `bug?` | Greps suspect locations and diagnoses. | `bug? saved-item count is off by one` |
| `qalist` | Pulls all open `needs-review` issues, P1-first, two sentences each. | `qalist` |
| `qa[NN]:` | Single-issue QA verdict. | `qa42: looks good, ship it` |

**Use these constantly.** A `q:` is faster than searching yourself, and it doesn't pollute your real session's context window.

**Slash commands (optional sugar).** This kit ships `/whatsnext`, `/qa`, `/plan`, and `/audit` under `.claude/commands/` — thin wrappers that run the same flows (`/whatsnext` = the §9 routine, `/qa` = `qalist` or a single verdict). They are Claude-Code-only convenience; your prefixes are the portable canon and work with any agent, including an offline or local one. Use whichever; they don't conflict.

---

## §5 · The "+" explore flag

Append `+` to any prefix when you want Claude to **look outward** — comparable products, industry conventions, UX patterns — and recommend.

```
decision+: how should the main view group items when there's nothing new?
q+: what do other apps in this space do when a user has zero items?
qa42+: passes, but is the empty state better as illustration or text?
```

You'll get **2–4 named options**, each with a real comparable and why it fits or doesn't fit this project specifically. Then "**Your call.**" Claude won't implement until you pick one.

Use `+` when you know *what* you want but not *how* it should look.

---

## §6 · The GitHub flow you don't have to think about

Claude handles the entire GitHub lifecycle. On its own:

- **One issue per session.** If you start without an issue, Claude opens one and assigns it to you.
- **One branch per session.** Branch name is whatever Claude Code auto-picks (`claude/<slug>-XXXX`). The issue ref lives in commit prefixes and the PR body, not the branch name.
- **Every commit references the issue.** `[#42] add saved-items tab`.
- **Claude pushes the feature branch and auto-opens the PR** when work is done. The body includes `Closes #NN` so the issue auto-closes on merge.
- **Labels are managed for you** — `needs-review` after a build, `qa-pass` / `qa-improve` / `qa-fail` after the verdict.

What you do: **review the PR** and **squash-merge** when CI is green and you've approved. `main` is PR-only — no direct push, no force-push, ever. If you close an issue directly on GitHub, apply the `human-closed` label first so Claude treats it as owner-approved.

> **Outside feedback** (optional): the pipeline ships a dormant feedback-scribe. If you name an external feedback provider in `CLAUDE.md` §3, their `Name:` prefix turns raw feedback into a tidy, labelled GitHub issue assigned to you. Off until you name someone.

---

## §7 · QA in 30 seconds

When a build session ends, Claude posts a **QA Brief** as a comment on the issue and pastes it into the PR body. Plain English — what was built, what to look for, where it shows up. You test, then reply with one of three verdicts:

| Verdict | Meaning | What happens |
|---|---|---|
| `qa-pass` | Ships. | Issue closes with `qa-pass`. PR squash-merges. Done. |
| `qa-improve` | Almost — small fixes needed. | Issue stays open. Claude writes a new SPEC, opens a follow-up build issue. |
| `qa-fail` | Wrong direction. | Issue stays open. Claude re-plans. |

Trigger verdicts in chat with `qa42: <free-form thoughts>` — Claude maps the free-form to a label and posts the structured comment. **Shortcut:** `qa-pass` can be applied directly on GitHub (close + label) — no chat needed.

---

## §8 · Teach Claude as you go

**`CLAUDE.md` is alive.** Every time something goes wrong, the right move is to teach Claude so it doesn't go wrong again.

**1. Catch a repeat mistake.**

> "You keep hardcoding strings in mockup screens. Add a failure mode for it."

Claude adds a row to `management/failure-modes.md` (`CLAUDE.md` §13 points there). Next session, Claude greps it and avoids it.

**2. Notice a workflow you reinvent every session.**

> "Every Plan session ends with me asking which file the SPEC should live in. Make that automatic."

Claude updates `CLAUDE.md` §8 (Spec flow) so it happens by default.

**3. A rule fires too often or not enough.**

> "The `+` flag should default on for any decision-style question."

Claude rewrites §2 to match. Trust this — small tweaks compound fast.

**Rule of thumb:** fixed the same Claude mistake twice? That's a failure-modes row. Typed the same instruction every session? That's a §1-§9 update.

---

## §9 · When it goes sideways

- **Claude is reading too many files at session start.** Tell it to re-read `CLAUDE.md §0` (the routing table); a routing rule likely needs trimming.
- **Claude tried to push to `main` or force-push.** Tell it no, and add a failure-modes row. `main` is PR-only, squash-merge.
- **Claude is mixing flavors** (planning *and* building at once). Stop, split into two issues, start fresh.
- **Claude opened a Build session before the stack lands.** Per `CLAUDE.md` §0.1 this should halt — if it didn't, that's a failure-modes row.
- **GitHub MCP is down.** Claude switches to local-only and lists the GitHub writes you need to do by hand.
- **Claude says "halt — missing reference file."** A file like `PROJECT.md` or a template was deleted or renamed. Don't ask Claude to improvise from memory — restore from git, then resume.

---

## §10 · The one rule for you

**If something is unclear, say so. Don't guess what the spec means and don't let Claude guess either.**

The whole pipeline is built around one idea: ambiguity is the enemy. Claude is told to stop and ask when a spec is fuzzy. Do the same in reverse — if Claude's plan looks off, push back in one sentence before it writes code. One question now beats a `qa-fail` an hour from now.

Everything else — branches, commits, labels, QA Briefs, SPECs, the whole `CLAUDE.md` — Claude handles. You just chat.

---

*Companion files: `CLAUDE.md` (the operating file Claude reads), `PROJECT.md` (project context), `management/templates/SPEC.md` and `management/templates/QA_BRIEF.md` (canonical formats), `DEVLOG.md` (decisions log).*
