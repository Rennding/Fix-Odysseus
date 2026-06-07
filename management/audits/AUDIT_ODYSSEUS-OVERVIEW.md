# Audit — What Odysseus Is, What It Does, and How to Operate It

*Plain-English orientation for Aram. Written 2026-06-07. Every technical term
gets a one-sentence explanation the first time it appears.*

---

## 1. What Odysseus is, in one breath

Odysseus is a **self-hosted AI workspace** — think "your own private ChatGPT,
but it runs on your computer instead of someone else's, and it can do far more
than chat."

- **Self-hosted** = it runs on hardware you control (your Fedora machine), not
  on a company's cloud. Your data never leaves your house unless you tell it to.
- It's built to feel like the ChatGPT / Claude web apps, but bolted onto a pile
  of extra tools: research, email, calendar, notes, a document editor, and an
  "agent" that can actually *do* tasks rather than just talk.

The author (the PewDiePie-archdaemon project) describes it as "the self-hosted
version of the UI experience you get from ChatGPT and Claude. But with more jank
and fun." That honesty matters — it works, but it's a fast-moving hobby project
with rough edges (their own roadmap literally opens with "SQUASH BUGS").

**The key idea:** you bring your own AI brain (a "model"), and Odysseus is the
body — the interface, memory, and tools wrapped around it.

- A **model** = the actual AI (the thing that generates text). Odysseus doesn't
  include one; it connects to one you run or pay for.
- You can plug in a **local model** (runs on your own GPU, fully private, free
  to run) or a **cloud API model** (like OpenAI's GPT or Anthropic's Claude —
  you pay per use, but it's smarter and needs no GPU).

---

## 2. What it enables for you

Here's what having Odysseus running actually gives you, feature by feature, in
human terms:

| Feature | What it actually does for you |
|---|---|
| **Chat** | Talk to any AI model through one clean interface. Swap between a free local model and a paid cloud one with a dropdown. |
| **Agent** | Hand the AI a *task* (not just a question) and let it run — it can search the web, read/write your files, run shell commands, and use tools on its own until the job's done. This is the "do it for me" mode. |
| **Cookbook** | Scans your computer's hardware, tells you which AI models will actually fit and run well, then downloads and starts them with a click. Removes the guesswork of "will this model run on my GPU?" |
| **Deep Research** | Give it a topic; it runs many web searches, reads the sources, and writes you a structured visual report. Like having a research assistant. |
| **Compare** | Run the same question through several models side-by-side, blind (names hidden), so you can judge which is best without bias. |
| **Documents** | A multi-tab text/markdown editor where the AI assists *you* (suggestions, edits) rather than writing everything for you. |
| **Memory / Skills** | The AI remembers facts about you across sessions, and builds up reusable "skills" (saved procedures) so it gets better at your recurring tasks over time. |
| **Email** | A full inbox (connects to your real email) with AI triage: auto-summaries, auto-tagging, urgency flags, draft replies, spam filtering. |
| **Notes & Tasks** | Quick notes with reminders, a todo list, and scheduled tasks the agent can actually act on (e.g. "every morning, summarize my inbox"). |
| **Calendar** | A local calendar that can sync with standard calendar servers (Apple, Nextcloud, Fastmail, etc.). |
| **Mobile** | Works on your phone as an installable app (a **PWA** = a website that installs and behaves like a native app). |
| **Extras** | Image editor, theme editor, file uploads the AI can *see* (images + PDFs), web search, 2FA login. |

**The honest summary of value:** Odysseus turns one box on your network into a
private, all-in-one AI cockpit — chat + autonomous agent + research + email +
calendar + notes — with no monthly subscription and no data leaving your control
(if you use local models).

---

## 3. Example use cases

Concrete ways this earns its keep:

1. **Private AI for sensitive work.** Draft, summarize, or analyze documents you
   would never paste into ChatGPT (legal, financial, personal). With a local
   model, nothing leaves your machine.
2. **Inbox autopilot.** Connect your email; let it triage overnight — summarize
   threads, flag what's urgent, pre-draft replies you just review and send.
3. **Research dossiers.** "Give me a briefing on X" → Deep Research returns a
   sourced report instead of you opening 30 tabs.
4. **A do-it agent.** "Find all PDFs in this folder, pull the invoice totals,
   and write them to a spreadsheet" — the agent uses its file + shell tools to
   carry it out.
5. **Model shopping without the headache.** Cookbook tells you exactly which
   models your hardware can run, so you stop downloading 40GB files that crash.
6. **Model bake-offs.** Use Compare to decide blind which model is best for your
   actual prompts before committing to one.
7. **A second brain.** Notes + Memory + scheduled tasks = an assistant that
   remembers your context and acts on a schedule.

---

## 4. Open problems & obvious bugs

This combines what the project openly documents with a light scan of the code in
the priority areas. The fork exists specifically to fix the first three.

### The headline bug we're here to fix (P0): Ollama tool-calling is unreliable

- **Ollama** = the most popular, easiest way to run a local AI model on your own
  machine.
- **Tool-calling** = the AI's ability to *use tools* (search, files, shell)
  instead of only chatting. It's what makes "Agent" mode work.
- **The problem:** when the agent uses a local Ollama model, the tool use often
  breaks — the agent stalls or quits a task immediately.

The diagnosed root cause (confirmed against the code):

- There are **two ways** to tell a model about its tools:
  1. **Native tool schemas** = a formal, structured machine format (the way
     OpenAI/Claude expect).
  2. **Fenced blocks** = the model just writes the tool call as a normal code
     block in its text, and Odysseus reads it back out.
- Local Ollama models **choke on native schemas** — many respond by emitting a
  single tool-call token and then stopping, so the agent loop "sees 1 token and
  no recognised tool, and the round terminates immediately" (the code itself
  cites this as issue #1567, in `src/agent_loop.py` ~line 1617). The **fenced**
  mode is what reliably works for them.
- So the fix logic (in `src/agent_loop.py` ~lines 1577–1637) tries to force
  Ollama endpoints down the fenced path. That logic is intricate and brittle:
  it juggles a per-endpoint `supports_tools` flag, a hardcoded keyword list of
  model names, a "no tools" blocklist, and URL sniffing — lots of moving parts
  that can disagree.
- A related piece: the **model-list cache** (Odysseus remembers which models an
  endpoint has, to avoid re-asking constantly) **doesn't refresh when you pull a
  new model** — so a model you just downloaded won't appear until something
  forces a refresh (`routes/model_routes.py` has the refresh-mode logic, and
  proxies default to manual/cached-first).

### P1: Skill auto-generation is too eager

- **Skills** = saved how-to procedures the AI writes for itself so it can repeat
  a task next time.
- The auto-generation lives in the **teacher-escalation loop**
  (`src/teacher_escalation.py`): when a weak local model fails a task, Odysseus
  calls a smarter "teacher" model that both fixes the answer *and* writes a new
  SKILL.md file.
- **The problem:** it mints a fresh draft skill on repeated/similar failures
  with no real **dedup** (deduplication = noticing "I already have a skill for
  this" and not making a copy). Result: duplicate, near-identical skills pile up.
- It needs gating (only save when genuinely new/useful) and dedup against
  existing skills before writing.

### P2: UX papercuts

- Small annoyances. The named example: the **model dropdown doesn't refresh
  after `ollama pull`** (same root cause as the cache issue above) — you
  download a model and it's not selectable until a reload.

### Broader known problems (from the project's own ROADMAP)

The author is candid that these areas are shaky:

- **Cookbook reliability** across different machines/GPUs/drivers is the area
  "most likely to need work."
- **GPU passthrough** (letting the AI use your graphics card inside Docker) is a
  common, fiddly failure point — the README has a long troubleshooting section.
- **Agent prompt bloat** — on small local models, all the tool/skill/memory text
  eats up the model's limited "context window" (its short-term memory) before
  your actual request even starts.
- **Email performance** over slow mail servers feels sluggish.
- **Prompt-injection risk** — user-editable skills, notes, fetched web pages,
  etc. are untrusted; a malicious page could try to hijack the agent. (See
  `THREAT_MODEL.md`.) An open audit item.
- **CSS / layout fragility** — the styling is openly called a mess; popups and
  mobile layouts are brittle.
- **Degraded-state reporting** — when a dependency (ChromaDB, search, email) is
  down, the app doesn't always tell you clearly.

**Bottom line:** the *obvious, targeted* bugs are the P0/P1/P2 above — those are
real, code-confirmed, and fixable with small patches. The *broad* problems
(Cookbook portability, CSS, email perf) are bigger, fuzzier efforts the author
flags as ongoing help-wanted.

---

## 5. How to operate it — and how to QA our fixes

### 5a. The setup you have today

You're running Odysseus on **localhost on Fedora**, installed from the author's
own repo (`pewdiepie-archdaemon/odysseus`). That means:

- You're running **upstream code** — the original, *unfixed* version.
- Our fork (`Rennding/Fix-Odysseus`, this repo) is where we write the patches.
- **Therefore: your live instance does NOT contain our changes.** To test
  anything we build, you have to run *our* code, not the copy you have now.

This is the crux of your QA question. Below is the clean way to do it.

### 5b. Day-to-day operation (what you already mostly know)

- Open it at `http://localhost:7000` (Docker) or `:7860` (native macOS-style).
- First login uses the temporary admin password printed in the terminal — for
  Docker, find it with: `docker compose logs odysseus`.
- Everything else (adding models, email, search) is configured **inside the app**
  under **Settings** or the `/setup` flow — not in config files.
- To connect a local Ollama model, in **Settings** add the endpoint
  `http://localhost:11434/v1` (or `http://host.docker.internal:11434/v1` if
  Odysseus is in Docker and Ollama is on the host), and make sure Ollama is
  listening broadly: `OLLAMA_HOST=0.0.0.0:11434 ollama serve`.

### 5c. How to QA a fix we make (the important part)

The goal: run *our patched branch* on your Fedora box, reproduce the bug, and
confirm it's gone. Here is the recommended workflow.

**One-time setup: get our fork onto your machine, alongside (not on top of) your
current install.**

```bash
# Clone our fork into a SEPARATE folder so your working install stays intact
git clone https://github.com/Rennding/Fix-Odysseus.git
cd Fix-Odysseus
```

**Each time you want to test a specific fix:**

```bash
# 1. Get the latest, then switch to the branch the fix lives on.
#    (I'll always tell you the branch name + PR link when a fix is ready.)
git fetch origin
git checkout <branch-name>     # e.g. claude/loving-dirac-Nt3r7
git pull origin <branch-name>

# 2. Run THIS code. Two options:
```

**Option A — Docker (closest to a real install, fully isolated):**

```bash
# Use a different port so it won't collide with your existing instance on 7000
echo "APP_PORT=7001" >> .env
docker compose up -d --build      # --build is essential: it rebuilds with our code
# open http://localhost:7001, grab the admin password from:
docker compose logs odysseus
```

**Option B — Native Python (faster to iterate, good for quick checks):**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py
python -m uvicorn app:app --host 127.0.0.1 --port 7001
# open http://localhost:7001
```

> Run our fork on a **different port** (7001) than your daily instance (7000) so
> you can have both open and compare old-vs-fixed behavior directly.

**3. Reproduce and confirm.** For every fix I'll hand you a **QA Brief** — a
short, plain-English checklist of: what to click, what the bug looked like
before, and what "fixed" looks like now. You follow those steps in the
`:7001` instance.

- Example for the P0 Ollama fix: "Add your Ollama endpoint, switch to Agent
  mode, pick a local model, ask it to search the web. **Before:** it stalls or
  quits instantly. **After:** it actually runs the search and answers."

**4. Give a verdict.** You tell me **pass / improve / fail** (in chat, or as a
label on the GitHub issue). Pass → I close it and we move on. Improve/fail → I
write up what's next and patch again.

### 5d. The shortcut, if rebuilding is annoying

If spinning up a second instance each time is too much friction, the lighter
alternative is: I tell you exactly which **files** changed, and you copy just
those files into your existing install and restart it. This is faster but
messier (your install drifts from upstream) — fine for a quick look, not ideal
for a clean verdict. For anything UI-related I'll also attach a **screenshot**
from a running instance, so you can often eyeball "is this right?" before even
running it yourself.

### 5e. Recommended default

For trustworthy QA: **Option A (Docker on port 7001), rebuilt per branch.** It's
the most "real," it can't corrupt your daily instance, and it matches how a real
user would run the fix. Keep your `:7000` instance as the "before" reference.

---

## Appendix — Useful health-check commands

```bash
docker compose ps                                   # are the containers up?
docker compose logs --tail=120 odysseus             # recent app logs
docker compose logs odysseus | grep -E 'ChromaDB|MemoryVectorStore|DEGRADED'  # dependency health
```

The internal service ports (for reference): `7000` app, `8080` SearXNG (search),
`8091` ntfy (notifications), `8100` ChromaDB (memory index), `11434` Ollama.
