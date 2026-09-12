import pytest
from main import (
    parse_history_line,
    detect_typo,
    detect_redundant_flags,
    analyze_history,
    generate_report,
)


def test_parse_history_line_valid():
    result = parse_history_line("git status")
    assert result["valid"] is True
    assert result["command"] == "git"
    assert result["args"] == ["status"]
    assert result["raw"] == "git status"


def test_parse_history_line_empty():
    result = parse_history_line("")
    assert result["valid"] is False
    assert result["command"] == ""
    assert result["args"] == []


def test_parse_history_line_comment():
    result = parse_history_line("# this is a comment")
    assert result["valid"] is False
    assert result["command"] == ""
    assert result["args"] == []


def test_detect_typo_gitt():
    assert detect_typo("gitt") == "git"


def test_detect_typo_correct_command():
    assert detect_typo("git") == ""
    assert detect_typo("ls") == ""
    assert detect_typo("cd") == ""


def test_detect_typo_pythn():
    assert detect_typo("pythn") == "python"


def test_detect_typo_empty():
    assert detect_typo("") == ""


def test_detect_redundant_flags_git():
    redundant = detect_redundant_flags("git", ["--verbose", "--verbose", "status"])
    assert redundant == ["--verbose"]


def test_detect_redundant_flags_ls():
    redundant = detect_redundant_flags("ls", ["-l", "-l", "-a"])
    assert redundant == ["-l"]


def test_detect_redundant_flags_no_redundancy():
    redundant = detect_redundant_flags("git", ["status"])
    assert redundant == []


def test_detect_redundant_flags_unknown_command():
    redundant = detect_redundant_flags("unknown", ["-x", "-x"])
    assert redundant == []


def test_analyze_history_basic():
    history = "git status\ngitt log\n"
    result = analyze_history(history)
    assert result["total_lines"] == 2
    assert result["valid_entries"] == 2
    assert result["typo_count"] == 1
    assert result["redundant_count"] == 0
    assert any("gitt" in s and "git" in s for s in result["suggestions"])


def test_analyze_history_with_redundant_flags():
    history = "ls -l -l\n"
    result = analyze_history(history)
    assert result["typo_count"] == 0
    assert result["redundant_count"] == 1
    assert any("-l" in s for s in result["suggestions"])


def test_analyze_history_empty():
    result = analyze_history("")
    assert result["total_lines"] == 1
    assert result["valid_entries"] == 0
    assert result["typo_count"] == 0
    assert result["redundant_count"] == 0
    assert result["suggestions"] == []


def test_generate_report_contains_expected_strings():
    result = {
        "total_lines": 10,
        "valid_entries": 8,
        "typo_count": 2,
        "redundant_count": 1,
        "suggestions": ["Typo: gitt -> git", "Redundant flags: ['-l']"],
    }
    report = generate_report(result)
    assert "Total lines: 10" in report
    assert "Valid entries: 8" in report
    assert "Typos found: 2" in report
    assert "Redundant flags: 1" in report
    assert "Typo: gitt -> git" in report
    assert "Redundant flags: ['-l']" in report


def test_generate_report_no_suggestions():
    result = {
        "total_lines": 5,
        "valid_entries": 5,
        "typo_count": 0,
        "redundant_count": 0,
        "suggestions": [],
    }
    report = generate_report(result)
    assert "Typos found: 0" in report
    assert "Redundant flags: 0" in report
    assert "Suggestions:" in report
