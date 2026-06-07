# Fix-Odysseus

## What is Fix-Odysseus

A fork of **Odysseus** (`pewdiepie-archdaemon/odysseus`), a self-hosted AI workspace, maintained to fix and improve specific subsystems. The work is targeted patches to an existing codebase, not a greenfield build. Fixes may be offered back to upstream as PRs, so every patch stays minimal and style-respecting.

## Pending state (read first)

Right now, this repo holds the pipeline scaffold only. **No app code exists yet.** The immediate next step is to merge in the Odysseus fork. The first real session after that merge must:

1. Read the incoming codebase and confirm the structure matches what `CLAUDE.md` §4 and §14 assume (`app.py`, `routes/`, `src/`, `static/js/`, `docker-compose.yml`).
2. Correct §4 and §14 if the real layout differs.
3. Only then start on the P0 mission below.

Until the import lands, Build and Improve sessions halt per `CLAUDE.md` §0.1.

## Mission (priority order)

**P0: Fix Ollama tool-calling.** Local-model (Ollama) tool-calling is unreliable. Root cause already diagnosed (Aram will provide a detailed SPEC):

- Native tool schemas (`supports_tools=1`) break local models; the fenced-block mode works.
- The endpoint defaults to `endpoint_kind='proxy'`, which disables native tools.
- The model-list cache does not refresh when new models are pulled.

**P1: Tame skill auto-generation.** It is too eager and mints duplicate draft skills from repeated tasks. Needs dedup and gating.

**P2: UX papercuts.** Smaller fixes, for example the model dropdown not refreshing after `ollama pull`.

## Constraints

- **Upstream-PR-ready.** Upstream rejects agent PRs that ignore its visual style. Keep every patch minimal and style-respecting.
- **Screenshots for UI.** Any UI-touching change (CSS, or DOM code in `static/js/`) requires a screenshot from the running app, not just type-checks or a green gate. See `CLAUDE.md` §4.
- **Issue-first.** One issue per change, matching upstream's contribution ask and the pipeline's §7 lifecycle.

## Platform targets

Self-hosted web app, run via Docker Compose. Models are served externally (Ollama, llama.cpp, or vLLM).

## Stack

- **Backend:** Python 3.11, FastAPI, SQLite, ChromaDB. Entry point `app.py` (uvicorn).
- **Frontend:** vanilla JavaScript in `static/js/`. No framework, no build step.
- **Runtime:** Docker Compose services `odysseus`, `chromadb`, `searxng`, `ntfy`.
- **Validation gate:** see `CLAUDE.md` §4 (pytest, py_compile, node --check).

## Team

| Person | GitHub | Role |
|---|---|---|
| Aram | @Rennding | Project lead, dev, QA. Decides scope, gives QA verdicts, merges PRs. |
| Claude | (none) | Implementer. Patches the codebase, manages issues, opens PRs. |

## Folder map

Pipeline scaffold (current):

- `CLAUDE.md`: operating file, read every session.
- `PROJECT.md`: this file.
- `HOW_TO_USE.md`: how to drive sessions.
- `management/`: templates, specs, audits, failure modes.
- `scripts/`: label setup and tooling.
- `.github/workflows/ci.yml`: guarded CI (green on the scaffold, enforces the Python gate once code lands).

Incoming with the Odysseus fork (expected, confirm on import):

- `app.py`: FastAPI entry point.
- `routes/`: HTTP endpoints (P0 tool-calling logic).
- `src/`: core backend logic.
- `static/js/`: frontend DOM code.
- `docker-compose.yml`: service stack.
