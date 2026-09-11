# cmd-doctor

**Diagnose shell typos. Get instant command suggestions.**

[![CI](https://github.com/cypherkeolis/cmd-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/cypherkeolis/cmd-doctor/actions)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/cypherkeolis/cmd-doctor/releases)

`cmd-doctor` is a lightweight CLI utility that analyzes failed shell commands to suggest the most likely intended executable. By leveraging Levenshtein distance and a comprehensive list of common system binaries, it helps users quickly correct typos without executing any commands.

## Features

- **Typo Correction**: Uses Levenshtein distance to find the closest matching installed executable.
- **Safe & Non-Interactive**: Suggests corrections only; never executes the suggested command.
- **Comprehensive Database**: Checks against a wide range of standard Unix/Linux utilities, development tools, and package managers.
- **Argument Preservation**: Automatically appends original command arguments to the suggested command.
- **Fast**: Optimized distance calculation for quick feedback.

## Installation

You can install `cmd-doctor` directly from source:

```bash
git clone https://github.com/cypherkeolis/cmd-doctor.git
cd cmd-doctor
```

No external dependencies are required beyond the Python standard library.

## Usage

Run the tool with Python 3:

```bash
python main.py
```

**Example Output:**

```text
Failed command: lss /home/user
Suggestions:
  ls /home/user
```

The tool currently runs with a hardcoded example command (`lss /home/user`) for demonstration purposes. To integrate into your own workflow, import the `suggest_command` function:

```python
from main import suggest_command, get_installed_executables

failed_cmd = "grepp pattern file.txt"
executables = get_installed_executables()
suggestions = suggest_command(failed_cmd, executables)

for suggestion in suggestions:
    print(suggestion)
```

## Running the Tests

The project includes a comprehensive test suite using `pytest`. To run the tests:

1. Install pytest (if not already installed):
   ```bash
   pip install pytest
   ```

2. Run the test suite:
   ```bash
   pytest
   ```

## License

This project is licensed under the MIT License.

```text
MIT License

Copyright (c) 2024 cypherkeolis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
