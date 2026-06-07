"""Tests for workspace operating-file auto-loading (CLAUDE.md / AGENTS.md).

When a workspace is set and it contains an operating file, agent_loop injects
that file into the system prompt so the agent follows it without being told to.
"""
import os

from src.agent_loop import (
    _load_workspace_instructions,
    _build_workspace_instructions_note,
    _build_workspace_tree,
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


def test_tree_lists_files_and_subfolders(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("x")
    sub = tmp_path / "indie-ops"
    sub.mkdir()
    (sub / "CURRICULUM.md").write_text("y")
    tree = _build_workspace_tree(str(tmp_path))
    assert "CLAUDE.md" in tree
    assert "indie-ops/" in tree
    assert "indie-ops/CURRICULUM.md" in tree


def test_tree_skips_hidden_and_vcs(tmp_path):
    (tmp_path / "keep.md").write_text("x")
    (tmp_path / ".secret").write_text("x")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("x")
    tree = _build_workspace_tree(str(tmp_path))
    assert "keep.md" in tree
    assert ".secret" not in tree
    assert ".git" not in tree


def test_tree_respects_depth(tmp_path):
    deep = tmp_path / "a" / "b" / "c" / "d"
    deep.mkdir(parents=True)
    (deep / "deep.md").write_text("x")
    tree = _build_workspace_tree(str(tmp_path))
    # depth cap is 2, so a/ and a/b/ appear but the deeply nested file does not.
    assert "a/" in tree
    assert "deep.md" not in tree


def test_tree_empty_for_missing_dir():
    assert _build_workspace_tree("/no/such/dir") == ""
    assert _build_workspace_tree("") == ""
