# QA Brief template

<!-- Canonical QA Brief format. Reference by path from CLAUDE.md §9. Posted as a GitHub comment on the build issue when build is done, and pasted into the PR body under `## QA Brief`. Never copy this template's body into the comment header — only fill the four labelled fields. -->

## Format

```
**Changed:** <user-facing summary, plain English>
**Test:** <numbered steps>
**Risks:** <observable symptoms>
**Gate:** `<validation gate — see CLAUDE.md §4>` — PASS / FAIL
```

## Voice rules

QA Briefs are operational documents, not product copy. They are always in **English** — the operating language of every project under this pipeline. If the product surface uses a different language, that split is documented in `PROJECT.md` under Languages; it never bleeds into the QA Brief.

- No function names. No file paths. No dev jargon.
- Write for someone with no memory of the issue existing — they open the app and need to know what changed and exactly where to look.
- Risks are what the user would *see* if it went wrong, not internal failure modes.
- Field labels (`**Changed:**`, `**Test:**`, `**Risks:**`, `**Gate:**`) and all body text are English.

### Worked example (npm stack shown; use your project's gate)

```
**Changed:** Saved items now appear in a new "Saved" tab in the bottom navigation. On first open the tab is empty with a short hint; tapping the bookmark icon on any item adds it there.

**Test:**
1. Open the app to the main list.
2. Tap the bookmark icon on any item.
3. Open the new "Saved" tab in the bottom navigation; confirm the item appears there.
4. Tap the bookmark icon again; confirm the item disappears from "Saved".
5. Close and reopen the app; confirm saved items persist.

**Risks:** Saved tab stays empty after bookmarking. Item appears twice. Saved items lost after reopening the app. Bookmark icon does nothing on tap.

**Gate:** `npm run check` — PASS
```

## Pre-post checklist

Before pasting the comment:

1. `Changed:` reads like a release note, not a commit message.
2. `Test:` steps are numbered, runnable on a real device or in a browser, and start from a known state ("Open the app to the main view…").
3. `Risks:` items are observable symptoms ("the value shows blank", "tap does nothing"), not "the X service threw".
4. `Gate:` line shows actual PASS / FAIL — never paste the template's `PASS / FAIL` text unedited. The gate command comes from `CLAUDE.md` §4 (until the stack is chosen it reads `<validation gate, TBD>`).
5. The four labels are bold (`**Changed:**` etc.) and on their own lines.
6. All text is English.
