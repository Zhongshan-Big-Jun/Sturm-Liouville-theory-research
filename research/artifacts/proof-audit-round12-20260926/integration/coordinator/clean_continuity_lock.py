from pathlib import Path
import fcntl, json

O = Path('/mnt/f/tools/math-audit-round12-20260926')
R = Path('/mnt/f/LaTeX/BVE research')
B = json.loads((O / 'baseline.json').read_text())
name = '.research-state/progress.lock'
if name in B['tracked'] or name in B['untracked']:
    raise RuntimeError('Original lock must not be removed')
if not (O / 'checkpoint-result.json').exists():
    raise RuntimeError('Continuity writer has not completed')
lock = R / name
existed = lock.exists()
if existed:
    with lock.open('r+b') as f:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if f.read() != b'':
            raise RuntimeError('Nonempty continuity lock requires inspection')
        (O / 'removed-empty-progress.lock').write_bytes(b'')
        lock.unlink()
        fcntl.flock(f, fcntl.LOCK_UN)
result = dict(status='PASS', path=name, existed=existed, removed=existed,
              scope='Only the newly created empty continuity lock, after checkpoint writer completion and successful nonblocking exclusive lock acquisition in the same private POSIX runtime.')
(O / 'continuity-lock-cleanup.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result), flush=True)
