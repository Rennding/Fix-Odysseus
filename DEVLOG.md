# Fix-Odysseus DEVLOG

Human-facing decisions log. Never read by Claude at session start (`CLAUDE.md` §0).
Sessions mirror decisions here per `CLAUDE.md` §10: GitHub first, local second.

Repo: https://github.com/Rennding/Fix-Odysseus

## Decisions log

- **2026-06-07 · Bootstrap.** Initialized Fix-Odysseus from the attended-pipeline template. Platform: self-hosted web. Stack: Python 3.11 / FastAPI / SQLite / ChromaDB backend, vanilla-JS frontend, Docker Compose runtime. The project is a fork of Odysseus (`pewdiepie-archdaemon/odysseus`); importing the fork's codebase is the immediate next step. Mission: P0 fix Ollama tool-calling, P1 skill auto-generation dedup, P2 UX papercuts.
- **2026-06-07 · Codebase import.** Merged the Odysseus fork (`Rennding/odysseus`) into the pipeline repo. Snapshot import (Aram's call) — today's code only, no fork history carried over (history still lives in the standalone `odysseus` repo). 944 tracked files. Collisions resolved: kept the fork's `README.md`, its CI workflow, and its issue/PR templates; folded the pipeline's `scripts/setup-labels.sh` into the fork's `scripts/`; preserved all pipeline operating files (`CLAUDE.md`, `PROJECT.md`, `HOW_TO_USE.md`, `DEVLOG.md`, `AGENTS.md`, `management/`). Confirmed structure and corrected `CLAUDE.md` §4/§14 and `PROJECT.md` to the real recursive layout (`src/` `core/` `services/` subdirs; `static/app.js` + `static/js/**`). Build/Improve sessions unblocked.

## Versions

- _(none yet; first version lands after the first P0 patch.)_
