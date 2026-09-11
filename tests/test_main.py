import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from main import levenshtein, suggest_command, get_installed_executables, main


class TestLevenshtein:
    def test_identical_strings(self):
        assert levenshtein("hello", "hello") == 0

    def test_empty_strings(self):
        assert levenshtein("", "") == 0

    def test_one_empty(self):
        assert levenshtein("abc", "") == 3
        assert levenshtein("", "abc") == 3

    def test_single_char_diff(self):
        assert levenshtein("cat", "bat") == 1

    def test_insertion(self):
        assert levenshtein("cat", "cats") == 1

    def test_deletion(self):
        assert levenshtein("cats", "cat") == 1

    def test_multiple_diffs(self):
        assert levenshtein("kitten", "sitting") == 3

    def test_completely_different(self):
        assert levenshtein("abc", "xyz") == 3

    def test_symmetric(self):
        assert levenshtein("abc", "xyz") == levenshtein("xyz", "abc")

    def test_empty_to_nonempty(self):
        assert levenshtein("", "a") == 1
        assert levenshtein("a", "") == 1


class TestSuggestCommand:
    def test_basic_typo_correction(self):
        executables = ["/usr/bin/ls", "/usr/bin/cat", "/usr/bin/grep"]
        suggestions = suggest_command("lss /home/user", executables)
        assert "ls /home/user" in suggestions

    def test_multiple_suggestions_sorted_by_distance(self):
        executables = ["/usr/bin/ls", "/usr/bin/cat", "/usr/bin/cd"]
        suggestions = suggest_command("ls /home", executables)
        # "ls" is exact match (distance 0), "cd" is distance 2
        assert suggestions[0] == "ls /home"

    def test_no_suggestions_when_too_far(self):
        executables = ["/usr/bin/ls", "/usr/bin/cat"]
        suggestions = suggest_command("xyzwv /home", executables, max_distance=1)
        assert suggestions == []

    def test_empty_command(self):
        executables = ["/usr/bin/ls"]
        suggestions = suggest_command("", executables)
        assert suggestions == []

    def test_none_executables_skipped(self):
        executables = [None, "/usr/bin/ls", None]
        suggestions = suggest_command("lss /home", executables)
        assert "ls /home" in suggestions

    def test_max_distance_parameter(self):
        executables = ["/usr/bin/ls", "/usr/bin/lsof"]
        # "lss" to "ls" is distance 1, to "lsof" is distance 3
        suggestions = suggest_command("lss /home", executables, max_distance=1)
        assert "ls /home" in suggestions
        assert "lsof /home" not in suggestions

    def test_returns_max_5_suggestions(self):
        executables = [f"/usr/bin/cmd{i}" for i in range(10)]
        suggestions = suggest_command("cmd0 /home", executables, max_distance=5)
        assert len(suggestions) <= 5

    def test_preserves_arguments(self):
        executables = ["/usr/bin/grep"]
        suggestions = suggest_command("grepp pattern file.txt", executables)
        assert "grep pattern file.txt" in suggestions

    def test_exact_match(self):
        executables = ["/usr/bin/ls"]
        suggestions = suggest_command("ls /home", executables)
        assert "ls /home" in suggestions

    def test_multiple_tokens_only_first_checked(self):
        executables = ["/usr/bin/ls", "/usr/bin/cat"]
        # Only first token is compared
        suggestions = suggest_command("lss cat", executables)
        assert "ls cat" in suggestions


class TestGetInstalledExecutables:
    def test_returns_list(self):
        result = get_installed_executables()
        assert isinstance(result, list)

    def test_contains_paths_or_none(self):
        result = get_installed_executables()
        for item in result:
            assert item is None or isinstance(item, str)

    def test_ls_is_found_on_most_systems(self):
        result = get_installed_executables()
        # ls should be found on most Unix-like systems
        assert any(item and item.endswith("/ls") for item in result)


class TestMain:
    def test_main_runs_without_error(self, capsys):
        with patch('main.get_installed_executables', return_value=[None]):
            main()
        captured = capsys.readouterr()
        assert "Failed command:" in captured.out

    def test_main_with_suggestions(self, capsys):
        mock_execs = ["/usr/bin/ls"]
        with patch('main.get_installed_executables', return_value=mock_execs):
            main()
        captured = capsys.readouterr()
        assert "Suggestions:" in captured.out
        assert "ls /home/user" in captured.out

    def test_main_no_suggestions(self, capsys):
        with patch('main.get_installed_executables', return_value=[None]):
            main()
        captured = capsys.readouterr()
        assert "No suggestions found." in captured.out
