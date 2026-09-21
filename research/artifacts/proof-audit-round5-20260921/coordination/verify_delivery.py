from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import subprocess
import sys

ROOT = Path('/mnt/f/LaTeX/BVE research')
OUT = Path('/mnt/f/tools/math-audit-round5-20260921')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

base = json.loads((OUT / 'baseline.json').read_text())
expected = json.loads((OUT / 'stage-expected-sha256.json').read_text())
staged = json.loads((OUT / 'staged-verification.json').read_text())
assert staged['status'] == 'PASS'
document_check = json.loads((OUT / 'final-document-check.json').read_text())
assert document_check['status'] == 'PASS'
head = git('rev-parse', 'HEAD').decode().strip()
assert git('rev-parse', 'HEAD^').decode().strip() == base['head']
assert head != base['head']
committed = git('diff-tree', '--no-commit-id', '--name-only', '-r', '-z', 'HEAD').decode().rstrip('\0').split('\0')
assert set(committed) == set(expected)
assert not git('diff', '--cached', '--name-only', '-z')

# Read actual committed objects instead of trusting the earlier staging result.
objects = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
for name, digest in expected.items():
    objects.stdin.write((head + ':' + name + '\n').encode())
    objects.stdin.flush()
    header = objects.stdout.readline().split()
    assert len(header) == 3 and header[1] == b'blob', header
    left = int(header[2])
    actual_hash = hashlib.sha256()
    while left:
        chunk = objects.stdout.read(min(1_048_576, left))
        assert chunk
        actual_hash.update(chunk)
        left -= len(chunk)
    assert objects.stdout.read(1) == b'\n'
    assert actual_hash.hexdigest() == digest, name
    with (ROOT / name).open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest, name
objects.stdin.close()
assert objects.stdout.read() == b'' and objects.wait() == 0

current_status = git('status', '--porcelain=v1', '-z', '--untracked-files=all').decode()
assert current_status == base['status_z'], 'Post-commit status differs from original unrelated work'
for name, digest in base['untracked'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
protection = json.loads((OUT / 'protection-result.json').read_text())
for name in protection['original_dirty_preserved']:
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == base['tracked'][name], name

def remote_head(remote):
    result = git('ls-remote', '--exit-code', remote, 'refs/heads/main').decode().strip()
    sha, ref = result.split()
    assert ref == 'refs/heads/main' and sha == head, (remote, result, head)
    return remote, {'branch': ref, 'sha': sha, 'verification': 'actual git ls-remote'}

assert sys.argv[1:] in [[], ['--local-only']], sys.argv[1:]
local_only = sys.argv[1:] == ['--local-only']
if local_only:
    remotes = {}
else:
    with ThreadPoolExecutor(max_workers=2) as pool:
        remotes = dict(pool.map(remote_head, ['origin', 'fork']))

result = {
    'status': 'PASS', 'verified_at_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'LOCAL_COMMIT_ONLY' if local_only else 'DELIVERED_TO_BOTH_REMOTES',
    'baseline_head': base['head'], 'commit': head, 'committed_paths': len(expected),
    'actual_committed_blobs_and_worktree_match_manifest': True,
    'remote_heads': remotes, 'post_commit_status_matches_original_exactly': True,
    'original_untracked_preserved': len(base['untracked']),
    'original_dirty_preserved': protection['original_dirty_preserved'],
    'report': 'reports/proof-audit-round5-20260921/REPORT.md',
    'formalization_scope': 'Local sparse-polynomial trace and boundary algebra; not full Sobolev closure or Green integration formalization',
    'plugin_source_changed': False,
    'final_document_check': {'status': document_check['status'], 'new_links_checked': document_check['new_links_checked'], 'review_bundles_verified': len(document_check['review_receipts'])},
}
name = 'LOCAL_COMMIT_VERIFICATION.json' if local_only else 'DELIVERY.json'
(OUT / name).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
