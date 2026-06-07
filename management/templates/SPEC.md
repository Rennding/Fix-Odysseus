# SPEC template

<!-- Canonical SPEC template. Reference by path from CLAUDE.md §8. Do not copy this file's body into a SPEC — fill it in inside management/specs/SPEC_<TOPIC-NAME>.md. -->

## Naming

`management/specs/SPEC_<TOPIC-NAME>.md` — uppercase topic, hyphens between words. Example: `SPEC_MAIN-VIEW.md`.

## Form

```
SPEC: <feature name>
SOURCE_FILES: <files being read for context>
TARGET_FILES: <files being edited>

Summary: <1–2 sentences>
Context: <why this exists; link to audit if any>

Design:
  <architecture, data flow, canonical patterns to follow>

Build plan:
  #<id> REGION: <region> | FUNCTION: <function name>
        What: <2–4 sentences>
        Constraints: <gotchas, guards, failure modes>

  #<id> REGION: ...
        ...

Implementation order: #X → #Y → #Z
QA checklist: <numbered steps the QA can run on the device or in the browser>
Risks: <observable symptoms if it goes wrong>
Open questions: <only if any remain after revisions pass>

Validation: python -m pytest; python -m py_compile app.py routes/*.py src/*.py; node --check static/js/<changed-file>.js
Model: Sonnet | Opus  ← Sonnet for mechanical / UI / content; Opus for plan / audit / complex judgment
```

Every build issue body must also carry a `**Model:**` line near the top.

## Authoring checklist

Before writing the SPEC to disk:

1. Confirm with Aram once: "Any revisions?" — never ask "should I write it?"
2. Every numbered build item answers: what region, what function, what 2–4-sentence change, what constraints.
3. Implementation order is explicit even when linear.
4. QA checklist is runnable steps on a real device or in a browser, not dev jargon.
5. Risks are observable symptoms (what the user sees if it breaks), not internal failure modes.
6. Open questions section is omitted if empty — do not leave a placeholder.
