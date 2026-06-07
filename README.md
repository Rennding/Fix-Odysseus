# Fix-Odysseus

A fork of **Odysseus** (`pewdiepie-archdaemon/odysseus`), a self-hosted AI workspace, maintained to fix and improve specific subsystems. The work is targeted patches to an existing codebase, with fixes possibly offered back upstream.

**Status:** pipeline scaffold only. The Odysseus fork codebase is imported as the immediate next step; no app code exists here yet.

## Mission (priority order)

1. **P0:** Fix unreliable local-model (Ollama) tool-calling.
2. **P1:** Dedup and gate the over-eager skill auto-generation.
3. **P2:** UX papercuts (for example, the model dropdown not refreshing after `ollama pull`).

## Stack

- Backend: Python 3.11, FastAPI, SQLite, ChromaDB (`app.py`, uvicorn).
- Frontend: vanilla JavaScript in `static/js/` (no framework, no build step).
- Runtime: Docker Compose (`odysseus`, `chromadb`, `searxng`, `ntfy`); models served externally via Ollama, llama.cpp, or vLLM.

## How this repo runs

This project uses an attended Claude operating model: one issue per session, one branch, one PR, and a QA gate the lead controls. The rules live in these files:

- `CLAUDE.md`: the operating file Claude reads every session.
- `PROJECT.md`: project context, mission, and constraints.
- `HOW_TO_USE.md`: how to drive sessions.
- `management/templates/`: the SPEC and QA Brief formats.
- `DEVLOG.md`: human-facing decisions log.

## Team

| Person | GitHub | Role |
|---|---|---|
| Aram | @Rennding | Project lead, dev, QA. Decides scope, gives QA verdicts, merges PRs. |
| Claude | (none) | Implementer. Patches the codebase, manages issues, opens PRs. |
