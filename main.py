import shutil
import sys
from difflib import SequenceMatcher


def levenshtein(a, b):
    if len(a) < len(b):
        return levenshtein(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


def get_installed_executables():
    return [shutil.which(cmd) for cmd in ['ls', 'cd', 'cat', 'grep', 'find', 'rm', 'cp', 'mv', 'mkdir', 'echo', 'pwd', 'touch', 'chmod', 'chown', 'ps', 'kill', 'top', 'man', 'which', 'apt', 'pip', 'git', 'python', 'python3', 'node', 'npm', 'curl', 'wget', 'tar', 'zip', 'unzip', 'ssh', 'scp', 'rsync', 'docker', 'kubectl', 'helm', 'terraform', 'ansible', 'vim', 'nano', 'emacs', 'less', 'more', 'head', 'tail', 'wc', 'sort', 'uniq', 'cut', 'awk', 'sed', 'xargs', 'tee', 'tr', 'diff', 'patch', 'file', 'stat', 'du', 'df', 'free', 'uptime', 'whoami', 'id', 'groups', 'su', 'sudo', 'env', 'export', 'set', 'unset', 'alias', 'history', 'clear', 'reset', 'stty', 'tty', 'uname', 'hostname', 'ifconfig', 'ip', 'netstat', 'ss', 'ping', 'traceroute', 'nslookup', 'dig', 'host', 'route', 'arp', 'iptables', 'nftables', 'ufw', 'firewalld', 'systemctl', 'service', 'journalctl', 'dmesg', 'lsof', 'lscpu', 'lsblk', 'lsusb', 'lspci', 'lshw', 'dmidecode', 'hdparm', 'smartctl', 'iostat', 'mpstat', 'vmstat', 'pidstat', 'sar', 'perf', 'strace', 'ltrace', 'gdb', 'valgrind', 'cppcheck', 'clang-tidy', 'eslint', 'pylint', 'flake8', 'black', 'isort', 'mypy', 'pytest', 'tox', 'nox', 'poetry', 'pipenv', 'virtualenv', 'conda', 'uv', 'ruff', 'pyright', 'sphinx', 'mkdocs', 'jupyter', 'ipython', 'ipykernel', 'notebook', 'lab', 'qtconsole', 'tensorboard', 'wandb', 'mlflow', 'dvc', 'kaggle', 'colab', 'gcloud', 'aws', 'az', 'azcopy', 's3cmd', 'rclone', 'borg', 'restic', 'duplicity', 'rsnapshot', 'snap', 'flatpak', 'appimage', 'deb', 'rpm', 'pacman', 'dnf', 'yum', 'zypper', 'apk', 'opkg', 'nix', 'guix', 'brew', 'portage', 'emerge', 'xbps', 'urpmi', 'pacman', 'pacman-key', 'makepkg', 'pacman-conf', 'pacman-db', 'pacman-mirror', 'pacman-optimize', 'pacman-sysupgrade', 'pacman-upgrade', 'pacman-remove', 'pacman-query', 'pacman-search', 'pacman-install', 'pacman-build', 'pacman-keygen', 'pacman-keyring', 'pacman-mirrorlist', 'pacman-optimize', 'pacman-sysupgrade', 'pacman-upgrade', 'pacman-remove', 'pacman-query', 'pacman-search', 'pacman-install', 'pacman-build', 'pacman-keygen', 'pacman-keyring', 'pacman-mirrorlist']]


def suggest_command(failed_cmd, executables, max_distance=3):
    tokens = failed_cmd.split()
    if not tokens:
        return []
    suggestions = []
    for exe in executables:
        if not exe:
            continue
        exe_name = exe.split('/')[-1]
        dist = levenshtein(tokens[0], exe_name)
        if dist <= max_distance:
            suggestions.append((dist, exe_name, ' '.join([exe_name] + tokens[1:])))
    suggestions.sort(key=lambda x: x[0])
    return [s[2] for s in suggestions[:5]]


def main():
    failed_cmd = "lss /home/user"
    executables = get_installed_executables()
    suggestions = suggest_command(failed_cmd, executables)
    print(f"Failed command: {failed_cmd}")
    if suggestions:
        print("Suggestions:")
        for s in suggestions:
            print(f"  {s}")
    else:
        print("No suggestions found.")


if __name__ == '__main__':
    main()
