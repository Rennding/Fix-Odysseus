"""Tests for the fabricated-tool-result detector.

Weak/thinking models sometimes parrot the harness-only "[Tool execution
results]" marker and invent a command's output instead of running a tool. The
detector keys off that marker (which only the harness emits) to catch and reject
the faked run.
"""
from src.agent_loop import _fabricated_result_marker


def test_detects_plural_marker():
    text = "Let me read it.\n[Tool execution results]\n\nFake file contents here"
    assert _fabricated_result_marker(text) == "[Tool execution results]"


def test_detects_singular_marker():
    assert _fabricated_result_marker("[Tool execution result]") == "[Tool execution result]"


def test_detects_with_envelope_suffix():
    # The real envelope has trailing clarifier text; the model often parrots it.
    text = "[Tool execution results] (output of YOUR tool calls above)\n\nfake"
    assert _fabricated_result_marker(text) == "[Tool execution results]"


def test_none_for_clean_text():
    assert _fabricated_result_marker("I will run cat to read the curriculum.") is None


def test_none_for_empty_or_missing():
    assert _fabricated_result_marker("") is None
    assert _fabricated_result_marker(None) is None
