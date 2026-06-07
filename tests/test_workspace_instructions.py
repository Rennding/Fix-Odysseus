"""Tests for workspace operating-file auto-loading (CLAUDE.md / AGENTS.md).

When a workspace is set and it contains an operating file, agent_loop injects
that file into the system prompt so the agent follows it without being told to.
"""
import os

from src.agent_loop import (
    _load_workspace_instructions,
    _build_workspace_instructions_note,
)


def test_loads_claude_md(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# Operating file\nDo the thing.\n")
    res = _load_workspace_instructions(str(tmp_path))
    assert res is not None
    name, content, truncated = res
    assert name == "CLAUDE.md"
    assert "Do the thing." in content
    assert truncated is False


def test_case_insensitive_match(tmp_path):
    (tmp_path / "claude.md").write_text("lowercase name\n")
    res = _load_workspace_instructions(str(tmp_path))
    assert res is not None
    assert res[0] == "claude.md"


def test_agents_md_fallback(tmp_path):
    (tmp_path / "AGENTS.md").write_text("agents content\n")
    res = _load_workspace_instructions(str(tmp_path))
    assert res is not None
    assert res[0] == "AGENTS.md"


def test_claude_takes_priority_over_agents(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("claude\n")
    (tmp_path / "AGENTS.md").write_text("agents\n")
    res = _load_workspace_instructions(str(tmp_path))
    assert res is not None
    assert res[0] == "CLAUDE.md"


def test_truncation_respects_cap(tmp_path, monkeypatch):
    monkeypatch.setenv("ODYSSEUS_WORKSPACE_INSTRUCTIONS_MAXCHARS", "10")
    (tmp_path / "CLAUDE.md").write_text("x" * 100)
    res = _load_workspace_instructions(str(tmp_path))
    assert res is not None
    name, content, truncated = res
    assert truncated is True
    assert len(content) == 10


def test_missing_file_returns_none(tmp_path):
    assert _load_workspace_instructions(str(tmp_path)) is None


def test_missing_dir_returns_none():
    assert _load_workspace_instructions("/no/such/dir/anywhere") is None


def test_empty_workspace_returns_none():
    assert _load_workspace_instructions("") is None


def test_note_frames_as_instructions_not_summary():
    note = _build_workspace_instructions_note("CLAUDE.md", "BODY-TEXT", False)
    assert "CLAUDE.md" in note
    assert "BODY-TEXT" in note
    assert "Do NOT summarize" in note
    assert "--- BEGIN CLAUDE.md ---" in note
    assert "--- END CLAUDE.md ---" in note
    assert "truncated" not in note.lower()


def test_note_marks_truncation():
    note = _build_workspace_instructions_note("CLAUDE.md", "BODY", True)
    assert "truncated" in note.lower()
