import re
from collections import Counter

COMMON_COMMANDS = ['git', 'ls', 'cd', 'rm', 'cp', 'mv', 'mkdir', 'echo', 'cat', 'grep', 'find', 'sudo', 'python', 'pip', 'curl', 'wget', 'ssh', 'scp', 'tar', 'zip', 'unzip', 'chmod', 'chown', 'kill', 'ps', 'top', 'htop', 'vim', 'nano', 'less', 'head', 'tail', 'wc', 'sort', 'uniq', 'awk', 'sed', 'diff', 'patch', 'make', 'docker', 'kubectl', 'helm', 'terraform', 'ansible', 'brew', 'apt', 'yum', 'dnf', 'pacman', 'npm', 'yarn', 'pnpm', 'node', 'ruby', 'gem', 'cargo', 'rustc', 'go', 'java', 'javac', 'mvn', 'gradle', 'swift', 'xcodebuild', 'pod', 'carthage', 'spack', 'conda', 'mamba', 'nix', 'nix-shell', 'nix-env', 'nix-build', 'nix-instantiate', 'nix-store', 'nix-channel', 'nix-collect-garbage', 'nix-prefetch-url', 'nix-hash', 'nix-paths', 'nix-serve', 'nix-copy-closure', 'nix-copy', 'nix-ping', 'nix-store', 'nix-store', 'nix-store', 'nix-store', 'nix-store']

FLAG_PATTERNS = {
    'git': ['--verbose', '-v', '--dry-run', '-n', '--force', '-f', '--all', '-a', '--branch', '-b', '--remote', '-r', '--upstream', '-u', '--quiet', '-q', '--no-pager', '--no-color', '--color', '--help', '-h', '--version', '-V'],
    'ls': ['-l', '-a', '-h', '-R', '-t', '-s', '-c', '-u', '-i', '-n', '-p', '-d', '-A', '-F', '-r', '-S', '-X', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8', '-9', '-0', '-g', '-G', '-b', '-B', '-C', '-D', '-E', '-f', '-H', '-I', '-J', '-K', '-L', '-M', '-N', '-O', '-P', '-Q', '-T', '-U', '-V', '-W', '-Y', '-Z', '--color', '--no-color', '--help', '-h', '--version', '-V'],
}

def parse_history_line(line: str) -> dict:
    line = line.strip()
    if not line or line.startswith('#'):
        return {'raw': line, 'valid': False, 'command': '', 'args': []}
    parts = line.split()
    command = parts[0] if parts else ''
    args = parts[1:] if len(parts) > 1 else []
    return {'raw': line, 'valid': True, 'command': command, 'args': args}

def detect_typo(command: str) -> str:
    if not command:
        return ''
    for cmd in COMMON_COMMANDS:
        if command == cmd:
            return ''
        if len(command) >= 2 and (command in cmd or cmd in command):
            return cmd
        if len(command) >= 3:
            for i in range(len(cmd)):
                if command == cmd[:i] + cmd[i+1:]:
                    return cmd
                if command == cmd[:i] + cmd[i] + cmd[i]:
                    return cmd
    return ''

def detect_redundant_flags(command: str, args: list) -> list:
    redundant = []
    if command in FLAG_PATTERNS:
        valid_flags = FLAG_PATTERNS[command]
        seen = set()
        for arg in args:
            if arg.startswith('-'):
                if arg in seen:
                    redundant.append(arg)
                seen.add(arg)
    return redundant

def analyze_history(history_text: str) -> dict:
    lines = history_text.strip().split('\n')
    parsed = [parse_history_line(l) for l in lines]
    valid_entries = [p for p in parsed if p['valid']]
    typo_count = 0
    redundant_count = 0
    suggestions = []
    for entry in valid_entries:
        cmd = entry['command']
        args = entry['args']
        typo = detect_typo(cmd)
        if typo:
            typo_count += 1
            suggestions.append(f"Typo: '{cmd}' -> '{typo}' in: {entry['raw']}")
        redundant = detect_redundant_flags(cmd, args)
        if redundant:
            redundant_count += 1
            suggestions.append(f"Redundant flags: {redundant} in: {entry['raw']}")
    return {
        'total_lines': len(lines),
        'valid_entries': len(valid_entries),
        'typo_count': typo_count,
        'redundant_count': redundant_count,
        'suggestions': suggestions
    }

def generate_report(result: dict) -> str:
    lines = [
        f"Total lines: {result['total_lines']}",
        f"Valid entries: {result['valid_entries']}",
        f"Typos found: {result['typo_count']}",
        f"Redundant flags: {result['redundant_count']}",
        "Suggestions:",
    ]
    for s in result['suggestions']:
        lines.append(f"  - {s}")
    return '\n'.join(lines)

def test_typo_detection():
    assert detect_typo('gitt') == 'git'
    assert detect_typo('ls') == ''
    assert detect_typo('cd') == ''
    assert detect_typo('pythn') == 'python'

def test_flag_redundancy():
    assert detect_redundant_flags('git', ['--verbose', '--verbose', 'status']) == ['--verbose']
    assert detect_redundant_flags('ls', ['-l', '-l', '-a']) == ['-l']
    assert detect_redundant_flags('git', ['status']) == []
    assert detect_redundant_flags('unknown', ['-x', '-x']) == []

def test_parse_history_line():
    result = parse_history_line('git status')
    assert result['command'] == 'git'
    assert result['args'] == ['status']
    assert result['valid'] == True
    result2 = parse_history_line('')
    assert result2['valid'] == False
    result3 = parse_history_line('# comment')
    assert result3['valid'] == False

def test_report_generation():
    result = {
        'total_lines': 10,
        'valid_entries': 8,
        'typo_count': 2,
        'redundant_count': 1,
        'suggestions': ['Typo: gitt -> git', 'Redundant flags: [-l]']
    }
    report = generate_report(result)
    assert 'Total lines: 10' in report
    assert 'Typos found: 2' in report
    assert 'Redundant flags: 1' in report
    assert 'Typo: gitt -> git' in report

if __name__ == '__main__':
    sample_history = """git status
gitt log
ls -l -l
cd /tmp
pythn script.py
git --verbose --verbose status
"""
    result = analyze_history(sample_history)
    print(generate_report(result))
