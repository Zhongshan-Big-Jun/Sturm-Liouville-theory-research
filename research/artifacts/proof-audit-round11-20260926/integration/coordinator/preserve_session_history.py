from pathlib import Path
import hashlib, json, subprocess

R = Path('/mnt/f/LaTeX/BVE research')
O = Path('/mnt/f/tools/math-audit-round11-20260926')
A = R / 'research/artifacts/proof-audit-round11-20260926/integration'
name = 'state/AGENTS_SESSION_LOG.md'
baseline = json.loads((O / 'baseline.json').read_text())
original = subprocess.check_output(['git', 'cat-file', 'blob', baseline['head'] + ':' + name], cwd=R)
sha = lambda raw: hashlib.sha256(raw).hexdigest()
if sha(original) != baseline['tracked'][name]:
    raise RuntimeError('Original Git blob does not match baseline raw bytes')
current = (R / name).read_bytes()
normalized = original.replace(b'\r\n', b'\n')
if current.count(normalized) != 1:
    raise RuntimeError('Original history is not one exact unchanged text segment')
offset = current.index(normalized)
fixed = current[:offset] + original + current[offset + len(normalized):]
if fixed[offset:offset + len(original)] != original:
    raise RuntimeError('Raw history preservation failed')
(O / 'session-log-before-byte-preservation.md').write_bytes(current)
(R / name).write_bytes(fixed)
result = dict(status='PASS', path=name, baseline_head=baseline['head'],
              original_file_sha256=sha(original), original_bytes=len(original),
              inserted_at_byte=offset, preserved_original_as_exact_segment=True,
              before_sha256=sha(current), after_sha256=sha(fixed),
              scope='Restore the exact original mixed line endings inside the unchanged historical segment; retain only the two round11 additions around it.')
raw = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
(O / 'session-history-preservation.json').write_bytes(raw)
(A / 'session-history-preservation.json').write_bytes(raw)
(A / 'coordinator/preserve_session_history.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(result), flush=True)
