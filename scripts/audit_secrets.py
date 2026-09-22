"""Conservative pattern audit. Reports locations/types, never matched values.
Not a replacement for gitleaks or manual review. Run from repository root.
"""
import json
from pathlib import Path
import re
import subprocess

RULES = {
    'private_key': rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'google_api_key': rb'AIza[0-9A-Za-z_-]{35}',
    'google_refresh_token': rb'1//[0-9A-Za-z_-]{30,}',
    'github_token': rb'(?:gh[pousr]_[0-9A-Za-z]{30,}|github_pat_[0-9A-Za-z_]{40,})',
    'aws_access_key': rb'(?:AKIA|ASIA)[A-Z0-9]{16}',
    'oauth_client_id': rb'[0-9]+-[a-z0-9]+\.apps\.googleusercontent\.com',
    'secret_assignment': rb'''(?i)["']?(?:client_secret|refresh_token|access_token|api_key|password)["']?\s*[:=]\s*["'][^"'\r\n]{12,}["']''',
    'personal_windows_path': rb'(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s"\']+',
}


def matches(data):
    return [name for name, pattern in RULES.items() if re.search(pattern, data)]


def git(*args):
    return subprocess.check_output(['git', *args], stderr=subprocess.DEVNULL)


def audit():
    findings = []
    seen = set()
    commits = git('rev-list', '--all').decode().splitlines()
    for commit in commits:
        for entry in git('ls-tree', '-r', '-z', commit).split(b'\0'):
            if not entry:
                continue
            meta, path = entry.split(b'\t', 1)
            _, kind, oid = meta.split()
            if kind != b'blob' or (oid, path) in seen:
                continue
            seen.add((oid, path))
            data = git('cat-file', 'blob', oid.decode())
            kinds = matches(data)
            if kinds:
                findings.append(dict(scope='history', commit=commit, file=path.decode('utf8'), types=kinds))
    files = git('ls-files', '--cached', '--others', '--exclude-standard', '-z').decode().split('\0')
    for name in sorted(set(files)):
        p = Path(name)
        if name and p.is_file():
            kinds = matches(p.read_bytes())
            if kinds:
                findings.append(dict(scope='working_tree', file=name, types=kinds))
    # Inspect ignored credential locations without scanning private video datasets.
    local = set(Path('studio/youtube/secrets').glob('*'))
    local.update(Path('.').glob('**/.env'))
    for p in sorted(local):
        if p.is_file() and p.name != '.gitignore':
            findings.append(dict(scope='local_ignored', file=p.as_posix(),
                                 types=matches(p.read_bytes()) or ['credential_location']))
    report = dict(commits_scanned=len(commits), unique_blob_paths_scanned=len(seen),
                  method='known patterns; no entropy scan; all reachable refs, current files and local credential locations',
                  findings=findings)
    Path('docs/local').mkdir(parents=True, exist_ok=True)
    Path('docs/local/security-audit.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    audit()
