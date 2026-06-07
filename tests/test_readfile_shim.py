"""Tests for the read_file shell-command shim.

Small local models in fenced mode sometimes type `read_file "x"` as a bash
command (the read_file TOOL name used as a shell command). The shim defines
read_file as a shell function aliased to cat so the read succeeds instead of
failing with "read_file: not found" and the model fabricating contents.
"""
from src.tool_execution import _shim_misfired_file_tools


def test_shim_injects_for_read_file_command():
    out = _shim_misfired_file_tools('read_file "notes.md"')
    assert out.startswith('read_file() { cat -- "$@"; }\n')
    assert 'read_file "notes.md"' in out


def test_shim_injects_for_multiple_read_file_lines():
    src = 'read_file "a.md"\nread_file "b.md"'
    out = _shim_misfired_file_tools(src)
    assert out.count("read_file()") == 1  # one function def, both calls kept
    assert '"a.md"' in out and '"b.md"' in out


def test_shim_no_op_for_normal_commands():
    src = 'ls -R && cat CLAUDE.md'
    assert _shim_misfired_file_tools(src) == src


def test_shim_no_op_when_read_file_only_as_substring():
    # A path containing "read_file" must not trigger the shim — it only fires
    # when read_file is at the start of a line (a command position).
    src = 'cat ./my_read_file_helper.sh'
    assert _shim_misfired_file_tools(src) == src


def test_shim_handles_leading_whitespace():
    src = '    read_file CLAUDE.md'
    out = _shim_misfired_file_tools(src)
    assert out.startswith('read_file() { cat -- "$@"; }\n')


def test_shim_empty_content():
    assert _shim_misfired_file_tools("") == ""
