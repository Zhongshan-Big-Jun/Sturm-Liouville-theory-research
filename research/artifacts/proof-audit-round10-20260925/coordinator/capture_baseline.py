from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,hashlib,datetime,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def sha(n):
    with (R/n).open('rb') as f:return n,hashlib.file_digest(f,'sha256').hexdigest()
if (O/'baseline.json').exists():raise RuntimeError('Baseline already exists')
head=git('rev-parse','HEAD').decode().strip()
if head!='5bb6b2605122d2daf472863b4bec0f35a9c192e1':raise RuntimeError('Unexpected head '+head)
status=git('status','--porcelain=v1','-z','--untracked-files=all').decode()
tracked=git('ls-files','-z').decode().rstrip('\0').split('\0')
untracked=git('ls-files','--others','--exclude-standard','-z').decode().rstrip('\0').split('\0')
dirty=git('diff','--name-only','-z').decode().rstrip('\0').split('\0')
if git('diff','--cached','--name-only','-z'):raise RuntimeError('Initial index is not empty')
with ThreadPoolExecutor(max_workers=6) as pool:
    T=dict(pool.map(sha,tracked));U=dict(pool.map(sha,[n for n in untracked if n]))
if git('rev-parse','HEAD').decode().strip()!=head:raise RuntimeError('HEAD changed during baseline capture')
(O/'baseline.json').write_text(json.dumps(dict(head=head,captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),tracked=T,untracked=U,original_dirty=[n for n in dirty if n],status_z=status),ensure_ascii=False,indent=2)+'\n')
D=O/'submitted'; D.mkdir(exist_ok=True)
Input=Path('/mnt/c/Users/HuangZY/Downloads/sl_audit_round10')
for p in Input.iterdir():
    if p.is_file(): shutil.copyfile(p,D/p.name)
manifest=json.loads((D/'manifest.json').read_text())
for n,rec in manifest['files'].items():
    if hashlib.sha256((D/n).read_bytes()).hexdigest()!=rec['sha256']:raise RuntimeError('Audit hash mismatch '+n)
(O/'CURRENT.json').write_text(json.dumps(dict(status='IN_PROGRESS',baseline=head,stage='intake',objective='Verify and repair round10 spectral indexing and reflection-sector findings; scope propagation, isolated review and publication',pending=['repair shared root enumeration','repair pure reflection perturbations','regression and formal feedback','isolated reviews','tool library and research navigation','scoped origin then fork publication']),ensure_ascii=False,indent=2)+'\n')
print('Baseline captured',len(T),'tracked;',len(U),'original untracked;',len(dirty),'dirty',flush=True)
