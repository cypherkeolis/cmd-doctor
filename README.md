# cmd-doctor

[![CI](https://github.com/cypherkeolis/cmd-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/cypherkeolis/cmd-doctor/actions)
[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/cypherkeolis/cmd-doctor/releases)

**cmd-doctor** is a static analysis CLI tool that inspects shell command history files (e.g., `.bash_history`, `.zsh_history`) to identify typos, redundant flags, and common mistakes. Unlike tools that execute commands to fix errors, `cmd-doctor` provides a safe, read-only audit of your command history with actionable suggestions for correction.

## Features

- **Typo Detection**: Identifies common command typos (e.g., `gitt` instead of `git`, `pythn` instead of `python`) using fuzzy matching against a list of common commands.
- **Redundant Flag Detection**: Detects duplicate flags in commands (e.g., `ls -l -l`) for supported commands like `git` and `ls`.
- **History Parsing**: Robustly parses history lines, ignoring comments and empty lines.
- **Report Generation**: Generates a clear, human-readable report summarizing total lines, valid entries, detected issues, and specific suggestions.
- **Static Analysis**: No command execution; safe to run on any history file.

## Installation

```bash
git clone https://github.com/cypherkeolis/cmd-doctor.git
cd cmd-doctor
```

## Usage

Run the tool directly with Python:

```bash
python main.py
```

The script includes a sample history for demonstration. To analyze your own history file, you can import the functions in your own script:

```python
from main import analyze_history, generate_report

with open('.bash_history', 'r') as f:
    history_text = f.read()

result = analyze_history(history_text)
print(generate_report(result))
```

## Running the Tests

The project includes a comprehensive test suite using `pytest`.

```bash
pip install pytest
pytest
```

## License

MIT
